import requests


root = 'http://localhost:8080/'


def point(txt):
    txt = txt[1:] if txt[0] == '/' else txt
    return root + txt


def test_static_files_work():
    files = ['jquery.js', 'main.css', 'main.js',
             'normalize.css', 'skeleton.css']
    for file in files:
        r = requests.get(point('/static/'+file))
        assert r.status_code == 200
