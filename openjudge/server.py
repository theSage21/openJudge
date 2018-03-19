import asyncio
import aiohttp_cors
import aiohttp_jinja2
import jinja2
from aiohttp import web
from collections import defaultdict
from .auth import (is_authenticated, register,
                   generate_token, remove_token,
                   get_user_from_token)
import datetime
from .core import Attempt


db = None
workspace = None
wrapper_map = None
epoch = datetime.datetime.utcfromtimestamp(0)


async def check_auth(data, db):
    tok = data.get('token')
    if not (await is_authenticated(tok, db)):
        raise web.HTTPNotFound(reason='Not Logged in')


@aiohttp_jinja2.template('home.html')
async def home(request):
    questions = []
    async for q in db.questions.find().sort('qno'):
        questions.append(q['qid'])
    return {"questions": questions}


async def question(request):
    data = await request.json()
    await check_auth(data, db)
    qid = data.get('qid')
    q = await db.questions.find_one({"qid": qid},
                                    projection={"_id": False,
                                                'test_cases': False})
    if q is None:
        raise web.HTTPNotFound(reason='No such Question')
    return web.json_response({"statement": q['statement']})


async def new_attempt(request):
    data = await request.json()
    await check_auth(data, db)
    qid = data.get('qid')
    code = data.get('code')
    lang = data.get('lang')
    user_token = data.get('token')
    user = await get_user_from_token(user_token, db)
    wrap = wrapper_map.get(lang)
    attempt = Attempt(code, wrap, workspace, user, qid)
    await db.attempt_queue.insert_one(attempt.__dict__)
    return web.json_response({'attid': attempt.attid})


async def languages(request):
    return web.json_response({"languages": list(wrapper_map.keys())})


async def signup(request):
    data = await request.json()
    uname = data.get('uname')
    pwd = data.get('pwd')
    reg_ok, reason = await register(uname, pwd, db)
    if not reg_ok:
        raise web.HTTPNotFound(reason=reason)
    else:
        return web.json_response({})


async def login(request):
    data = await request.json()
    uname, pwd = data.get('uname'), data.get('pwd')
    tok_ok, tok = await generate_token(uname, pwd, db)
    if not tok_ok:
        raise web.HTTPNotFound(reason=tok)
    else:
        return web.json_response({"token": tok})


async def logout(request):
    data = await request.json()
    tok = data.get('token')
    await remove_token(tok, db)
    return web.json_response({})


async def score_calc(request):
    data = await request.json()
    uname = await get_user_from_token(data.get('token'), db)
    score = 0
    async for att in db.history.find({"user": uname}):
        score += 1 if att['status'] else 0
    return web.json_response({"score": score})


async def wait_for_verdict(request):
    data = await request.json()
    await check_auth(data, db)
    attid = data['attid']
    while True:
        att = await db.history.find_one({"attid": attid})
        if att is None:
            asyncio.sleep(1)
        else:
            return web.json_response({'status': att['status']})


async def leaderboard(request):
    history = defaultdict(list)
    async for attempt in db.history.find({"status": True}).sort('datetime'):
        att = Attempt()
        att.__dict__ = attempt
        stamp = att.datetime - epoch
        history[att.user].append((stamp.total_seconds(), 1))
    return web.json_response(history)


def run_server(port, host, database, static_folder,
               wrapmap, wkspace, template_path):
    global db, workspace, wrapper_map
    db = database
    workspace = wkspace
    wrapper_map = wrapmap
    app = web.Application()

    app.router.add_post('/login', login)
    app.router.add_post('/logout', logout)
    app.router.add_post('/signup', signup)
    app.router.add_post('/attempt', new_attempt)
    app.router.add_post('/question', question)
    app.router.add_get('/languages', languages)
    app.router.add_post('/score', score_calc)
    app.router.add_post('/wait/for/verdict', wait_for_verdict)
    app.router.add_get('/leader', leaderboard)
    app.router.add_get('/', home)
    # -----------cors

    corsconfig = {"*": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                                    expose_headers="*",
                                                    allow_headers="*")}
    cors = aiohttp_cors.setup(app, defaults=corsconfig)
    for route in list(app.router.routes()):
        try:
            cors.add(route)
        except Exception as e:
            print(e)  # /register will be added twice and will raise error

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(template_path))

    x = app.router.add_static('/static', static_folder)
    x = cors.add(x)
    web.run_app(app, host=host, port=port)
