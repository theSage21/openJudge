import bottle
from openjudge import tools, config

contest = tools.read_contest_json()
app = bottle.Bottle()


@app.get('/')
def home():
    return tools.render('home.html')


@app.get('/question/<pk>')
def question_display(pk):
    pk = str(pk)
    q = {'statement': 'This question does not exist'}
    if pk.isdigit():
        if pk in contest['questions'].keys():
            q = contest['questions'][pk]
    return tools.render('question.html', {'statement': q['statement']})


@app.get('/static/<path:path>')
def static_server(path):
    root = config.static_root
    return bottle.static_file(path, root=root)
