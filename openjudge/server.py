from aiohttp import web
import inspect
from peewee import IntegrityError
from functools import wraps
from . import database


def fill_args(function):
    spec = inspect.getfullargspec(function)
    args, defaults, anno = spec.args, spec.defaults, spec.annotations
    defaults = (
        set()
        if defaults is None
        else set([name for _, name in zip(reversed(defaults), reversed(args))])
    )

    @wraps(function)
    async def wrapped_fn(request):
        given = await request.json()
        kwargs = dict()
        for name in spec.args:
            if name not in given and name not in defaults and name != "request":
                raise web.HTTPBadRequest(
                    reason="Please provide `{name}`".format(name=name)
                )
            if name in given:
                val = given[name]
                val = anno.get(name, lambda x: x)(val)
            elif hasattr(request.app, name):
                val = request.app[name]
                val = anno.get(name, lambda x: x)(val)
                kwargs[name] = val
        final = await function(request, **kwargs)
        return final

    return wrapped_fn


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
        tok = Token.create(user=user)
    except IntegrityError:
        return web.HTTPTemporaryRedirect("/login")
    # TODO: set cookie


app = web.Application()
app.add_routes([web.post("/register", register), web.post("/login", login)])
# -------------------------
app["User"] = database.User
