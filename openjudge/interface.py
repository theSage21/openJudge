import bottle
from openjudge import tools, config, judge


app = bottle.Bottle()


def jget(*keys):
    "Needs to be used like a, b, c = jget(x, y, z)"
    return [bottle.request.json[key] for key in keys]


@app.get('/')
def home():
    with tools.Contest() as contest:
        d = {'languages': list(sorted(list(contest['wrappers'].keys()))),
             'questions': list(sorted(list(contest['questions'].keys()),
                                      key=lambda x: int(x))),
             'intro': contest['intro']
             }
    return tools.render('home.html', d)


@app.get('/static/<path:path>')
def static_server(path):
    root = config.static_root
    return bottle.static_file(path, root=root)


# ---------------------------------------------API
@app.post('/login')
def login():
    u, p = jget('username', 'password')
    status, token = tools.login_user(u, p)
    return {'status': status, 'token': token}


@app.post('/logout')
def logout():
    token, = jget('token')
    return {'status': tools.logout_user(token)}


@app.post('/register')
def register():
    u, p = jget('username', 'password')
    status = tools.register_user(u, p)
    return {'status': status}


@app.post('/question')
def question_display():
    pk, = jget('question_pk')
    statement = 'This question does not exist yet.'
    with tools.Contest() as contest:
        pk = str(pk)
        q = {'statement': 'This question does not exist'}
        if pk.isdigit():
            if pk in contest['questions']:
                q = contest['questions'][pk]
                statement = q['statement']
    return {'statement': statement}


@app.post('/attempt')
def question_attempt():
    qpk, lang, code, token = jget('question', 'language', 'code', 'token')
    user = tools.get_user(token)
    message, attid = 'Unexpected Error', None
    if user is not None:
        if tools.attempt_is_ok(qpk, lang, code):
            i, o = tools.get_question_io(qpk)
            wrap = tools.get_wrap(lang)
            attid = tools.random_id()
            judge.submit_attempt(code, i, o, wrap, attid, user, qpk)
            message = 'Submitted'
        else:
            message = 'Question/Language does not exist'
    else:
        message = 'Please login'
    # -------------------------------------------
    return {'attempt': attid, 'message': message}


@app.post('/attempt/status')
def attempt_status():
    attid, = jget('attempt')
    status, message = judge.get_attempt_status(attid)
    return {'status': status, 'message': message}


@app.post('/user/score')
def user_score():
    user, = jget('user')
    score = tools.get_user_score(user)
    return {'score': score}


@app.post('/user/leader')
def user_list():
    users = tools.get_all_users()
    data = [(tools.get_user_score(u), u) for u in users]
    data.sort(key=lambda x: x[0], reverse=True)
    return {'leader': data}


@app.post('/user/details')
def user_details():
    token,  = jget('token')
    user = tools.get_user(token)['name']
    score = tools.get_user_score(user)
    return {'user': user, 'score': score}
