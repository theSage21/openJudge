import bottle
from openjudge import tools, config

tools.update_contest_data()
app = bottle.Bottle()


@app.get('/')
def contest_home():
    return tools.render('contest.html')


@app.get('/static/<path:path>')
def static_server(path):
    root = config.static_root
    return bottle.static_file(path, root=root)
