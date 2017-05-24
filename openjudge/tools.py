import os
import json
import bottle
import random
import pkgutil
from shutil import copyfile
from openjudge import config

__all__ = ['log', 'section', 'render', 'setup_contest', 'read_contest_json']


def log(*args):
    print(*args)


def random_id(n=30):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    name = ''.join(random.choice(letters) for _ in range(n))
    return name


def section(text):
    log('='*100)
    log('.'*25, text)
    log('='*100)


def render(template, data=None):
    data = data if data is not None else dict()
    template_dir = config.template_root
    with open(os.path.join(template_dir, template)) as fl:
        html = fl.read()
    return bottle.template(html, **data)


def __copy_intro__():
    "Copy contest intro to static files"
    if not os.path.exists(config.static_root):
        os.mkdir(config.static_root)
    if not os.path.exists(os.path.join(config.variable_root, 'intro.txt')):
        message = "Intro.txt not found in {}".format(config.variable_root)
        raise Exception(message)
    copyfile(os.path.join(config.variable_root, 'intro.txt'),
             os.path.join(config.static_root, 'intro'))
    log('Copied intro.txt')
    with open(os.path.join(config.variable_root, 'intro.txt'), 'r') as fl:
        intro = fl.read()
    return intro


def __copy_templates__():
    "Copy contest templates into templates directory"
    if not os.path.exists(config.template_root):
        log('{} does not exist. Creating'.format(config.template_root))
        os.mkdir(config.template_root)
    for template in ['home.html', 'question.html', 'leader.html']:
        with open(os.path.join(config.template_root, template), 'w') as fl:
            html = pkgutil.get_data('openjudge',
                                    'templates/' + template).decode()
            fl.write(html)
        log('Copied {}'.format(template))


def __copy_static__():
    "Copy contest static into static directory"
    if not os.path.exists(config.static_root):
        log('{} does not exist. Creating'.format(config.static_root))
        os.mkdir(config.static_root)
    for static in ['normalize.css', 'skeleton.css']:
        with open(os.path.join(config.static_root, static), 'w') as fl:
            html = pkgutil.get_data('openjudge',
                                    'static/' + static).decode()
            fl.write(html)
        log('Copied {}'.format(static))


def __copy_questions__():
    "Copy questions from variable directory to database"
    if not os.path.exists(config.variable_root):
        message = "Variable directory not found in {}"
        message = message.format(config.variable_root)
        raise Exception(message)
    log('Variable Directory found')
    qdata = {}
    vr = config.variable_root
    for folder in sorted(os.listdir(vr)):  # QUESTION
        path = os.path.join(vr, folder)
        if os.path.isdir(path):
            log('Question number {} detected'.format(folder))
            with open(os.path.join(path, 'statement'), 'r') as fl:
                stmt = fl.read()
            log('statement read for {}'.format(folder))
            qdata[folder] = {'statement': stmt}
            io_data = {}
            for io in sorted(os.listdir(path)):
                if io[0] in 'io':
                    if io[1:] not in io_data.keys():
                        io_data[io[1:]] = {'in': '', 'out': ''}
                    with open(os.path.join(path, io), 'r') as fl:
                        if io[0] == 'i':
                            io_data[io[1:]]['in'] = fl.read()
                        elif io[0] == 'o':
                            io_data[io[1:]]['out'] = fl.read()
            log('{} are test cases found'.format(list(io_data.keys())))
            qdata[folder]['testcases'] = io_data
    return qdata


def __read_contest_wrappers__():
    "Copy contest wrappers"
    if not os.path.exists(config.variable_root):
        message = "Variable directory not found in {}"
        message = message.format(config.variable_root)
        raise Exception(message)
    vr = config.variable_root
    with open(os.path.join(vr, 'wrappers.json'), 'r') as fl:
        wrappers = json.load(fl)
    log('Read contest wrappers')
    return wrappers


def setup_contest():
    "Set up the contest"
    intro = __copy_intro__()
    __copy_templates__()
    __copy_static__()
    wrappers = __read_contest_wrappers__()
    qdata = __copy_questions__()
    contest_data = {'questions': qdata,
                    'intro': intro,
                    'wrappers': wrappers,
                    'attempts': {}
                    }
    with open('contest.json', 'w') as fl:
        fl.write(json.dumps(contest_data, indent=4))
    log('Contest Data Written to contest.json')
    return contest_data


def read_contest_json():
    if os.path.exists('contest.json'):
        with open('contest.json', 'r') as fl:
            contest = json.load(fl)
    contest = {}
    return contest


def add_attempt_to_contest(attemptid, attempt_details):
    if os.path.exists('contest.json'):
        contest = read_contest_json()
        if 'attempts' not in contest.keys():
            contest['attempts'] = {}
        contest['attempts'][attemptid] = attempt_details
        with open('contest.json', 'w') as fl:
            json.dump(contest, fl)
