from aiohttp import web
import asyncio
import base64
import inspect
from aiohttp_session import setup, get_session, session_middleware, new_session
from aiohttp_session import SimpleCookieStorage
from peewee import IntegrityError
from functools import wraps
from . import database
import json


def fill_args(function):
    spec = inspect.getfullargspec(function)
    args, defaults, anno = spec.args, spec.defaults, spec.annotations
    defaults = (
        set()
        if defaults is None
        else set([name for _, name in zip(reversed(defaults), reversed(args))])
    )

    async def wrapped_fn(request):
        given = await request.json()
        kwargs = dict()
        for name in spec.args:
            if (
                name not in given
                and name not in defaults
                and name != "request"
                and name not in request.app
            ):
                raise web.HTTPBadRequest(
                    reason="Please provide `{name}`".format(name=name)
                )
            if name in given:
                val = given[name]
                val = anno.get(name, lambda x: x)(val)
                kwargs[name] = val
            elif name in request.app:
                val = request.app[name]
                val = anno.get(name, lambda x: x)(val)
                kwargs[name] = val
        final = await function(request, **kwargs)
        return final

    wrapped_fn = wraps(function)(wrapped_fn)

    return wrapped_fn


def login_required(function):
    @wraps(function)
    async def new_function(request, *a, **kw):
        session = await get_session(request)
        request["session"] = session
        token = request.app["Token"].get_or_none(
            request.app["Token"].id == session["token_id"]
        )
        if token is None:
            return web.HTTPUnauthorized(reason="No such token")
        request["token"] = token
        return await function(request, *a, **kw)

    return new_function


@fill_args
async def register(request, User, name: str, pwd: str):
    try:
        user = User.create(name=name, pwd=pwd)
    except IntegrityError:
        return web.HTTPBadRequest(reason="Name already exists")
    return web.json_response({"uid": user.id})


@fill_args
async def login(request, User, Token, name: str, pwd: str):
    try:
        user = User.get(User.name == name, User.pwd == pwd)
    except User.DoesNotExist:
        return web.HTTPNotFound(reason="no such user")
    try:
        token = Token.create(user=user)
    except IntegrityError:
        return web.HTTPTemporaryRedirect("/login")
    session = await new_session(request)
    session["token_id"] = token.id
    return web.json_response({"ok": True})


@login_required
async def logout(request):
    request["token"].delete_instance()
    request["session"].invalidate()


@fill_args
async def job_is_done(
    request,
    AttemptCheck,
    checkid: str,
    stdout: str,
    stderr: str,
    exit_code: int,
    is_timeout: bool = False,
):
    try:
        check = AttemptCheck.get_by_id(checkid)
    except AttemptCheck.DoesNotExist:
        await asyncio.sleep(2)  # defensive rate limit
        return web.HTTPDoesNotExist(reason="no such check job issued")
    check.is_timeout = is_timeout
    check.exit_code = exit_code
    check.stdout = stdout
    check.stderr = stderr
    check.save()
    check.attempt.is_being_checked = False
    check.attempt.is_checked = True
    check.attempt.save()
    return web.json_response({"ok": True})


@fill_args
async def get_a_job(request, Attempt, AttemptCheck):
    attempts = list(
        Attempt.select()
        .where(Attempt.is_checked == False)
        .order_by(Attempt.is_being_checked == True)
        .limit(1)
    )
    if len(attempts) == 0:
        await asyncio.sleep(1)
        return web.HTTPTemporaryRedirect("/runnerjob")
    else:
        attempt = attempts[0]
        try:
            check = AttemptCheck.create(attempt=attempt)
        except IntegrityError:
            return web.HTTPTemporaryRedirect("/runnerjob")
        else:
            attempt.is_being_checked = True
            attempt.save()
            return web.json_response(
                {
                    "checkid": check.id,
                    "inp": attempt.testcase.inp,
                    "cmd": attempt.program.language.shell_cmd,
                    "code": attempt.program.code,
                    "timeout": attempt.testcase.question.time_limit
                    * attempt.program.language.time_multiplier,
                }
            )


async def app():
    @web.middleware
    async def add_cors(request, handler):
        origin = request.headers.get("Origin", "*")
        cors_string = "Origin, Accept , Content-Type, X-Requested-With, X-CSRF-Token"
        d = {
            "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
            "Access-Control-Allow-Headers": cors_string,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Origin": origin,
        }
        response = await handler(request)
        response.headers.update(d)
        return response

    async def cors(request):
        return web.Response(text="")

    app = web.Application(debug=True, middlewares=[add_cors])
    setup(app, SimpleCookieStorage())
    # -----------------------------------
    app.add_routes(
        [
            web.post("/register", register),
            web.post("/login", login),
            web.get("/logout", logout),
            web.get("/runnerjob", get_a_job),
            web.post("/runnerjob", job_is_done),
        ]
    )
    app.router.add_route("OPTIONS", "/{url:.*}", cors)
    # -----------------------------------
    app["User"] = database.User
    app["Token"] = database.Token
    app["Language"] = database.Language
    app["Program"] = database.Program
    app["Question"] = database.Question
    app["Contest"] = database.Contest
    app["ContestQuestion"] = database.ContestQuestion
    app["TestCase"] = database.TestCase
    app["Attempt"] = database.Attempt
    app["AttemptCheck"] = database.AttemptCheck

    return app
