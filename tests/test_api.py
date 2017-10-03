import requests
import pytest


root = 'http://localhost:8080/'


def point(txt):
    txt = txt[1:] if txt[0] == '/' else txt
    return root + txt


@pytest.fixture
def user():
    data = {'username': 'sample', 'password': 'pwd'}
    requests.post(point('register'), json=data)
    yield data


@pytest.fixture
def luser(user):
    r = requests.post(point('login'), json=user)
    yield r.json(), user
    requests.post(point('logout'), json={'token': r.json()['token']})


def test_static_files_work():
    files = ['jquery.js', 'main.css', 'main.js',
             'normalize.css', 'skeleton.css']
    for file in files:
        r = requests.get(point('/static/'+file))
        assert r.status_code == 200


def test_user_registration_works():
    data = {'username': 'sample', 'password': 'pwd'}
    r = requests.post(point('register'), json=data)
    assert r.status_code == 200
    assert r.json()['status'], r.json()


def test_login_works(user):
    r = requests.post(point('login'), json=user)
    assert r.status_code == 200
    requests.post(point('logout'), json={'token': r.json()['token']})


def test_user_logout_works(luser):
    toks, user = luser
    r = requests.post(point('logout'), json={'token': toks['token']})
    assert r.status_code == 200
