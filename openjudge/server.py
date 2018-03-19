import aiohttp_cors
import aiohttp_jinja2
import jinja2
from aiohttp import web
from .auth import (is_authenticated, register,
                   generate_token, remove_token,
                   get_user_from_token)
from .core import Attempt


db = None
workspace = None
wrapper_map = None


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
    return web.json_response({})


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
    # app.router.add_get('/score', setup)
    # app.router.add_get('/leader', setup)
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
