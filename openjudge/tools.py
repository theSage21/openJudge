import os
import json
import time
import bottle
import random
import pkgutil
from openjudge import config
from collections import defaultdict
from multiprocessing import Lock


__all__ = ['log', 'section', 'render', 'setup_contest', 'Contest']


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# UTILITY
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
class Contest(dict):
    "Use with `with`. In case of an exception, nothing is comitted"
    file_lock = Lock()
    def __enter__(self):
        if not os.path.exists(config.contest_json):
            with Contest.file_lock:
                with open(config.contest_json, 'w') as fl:
                    json.dump(config.default_contest, fl, indent=4)
        with Contest.file_lock:
            with open(config.contest_json, 'r') as fl:
                C = json.loads(fl.read())
        # _set it on self
        for k, v in C.items():
            self[k] = v
        return self

    def __exit__(self, type, value, trace):
        C = {k: v for k, v in self.items()}
        with Contest.file_lock:
            with open(config.contest_json, 'w') as fl:
                json.dump(C, fl, indent=4)
        return True


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

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Openjudge setup things
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


def __get_intro__():
    "Copy contest intro to static files"
    if not os.path.exists(os.path.join(config.variable_root, 'intro.txt')):
        message = "Intro.txt not found in {}".format(config.variable_root)
        raise Exception(message)
    log('Read intro.txt')
    with open(os.path.join(config.variable_root, 'intro.txt'), 'r') as fl:
        intro = fl.read()
    return intro


def __copy_templates__():
    "Copy contest templates into templates directory"
    if not os.path.exists(config.template_root):
        log('{} does not exist. Creating'.format(config.template_root))
        os.mkdir(config.template_root)
    for template in ['home.html']:
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
    for static in ['normalize.css', 'skeleton.css', 'main.js', 'main.css', 'jquery.js']:
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
    intro = __get_intro__()
    __copy_templates__()
    __copy_static__()
    wrappers = __read_contest_wrappers__()
    qdata = __copy_questions__()
    with Contest() as contest:
        contest['questions'] = qdata
        contest['intro'] = intro
        contest['wrappers'] = wrappers
        if 'attempts' not in contest:
            contest['attempts'] = {}
        if 'tokens' not in contest:
            contest['tokens'] = {}
        if 'users' not in contest:
            contest['users'] = {}
    log('Contest Data Written to contest.json')


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


def login_user(name, pwd):
    status, token = False, None
    with Contest() as contest:
        log(contest['users'])
        log(name, pwd)
        if name in contest['users']:
            if pwd == contest['users'][name]['password']:
                token = random_id(50)
                contest['tokens'][token] = name
                status = True
    return status, token


def logout_user(token):
    status = False
    with Contest() as contest:
        if token in contest['tokens']:
            contest['tokens'].pop(token)
            status = True
    return status


def register_user(name, pwd):
    status = False
    log('{} {} received for registration'.format(name, pwd))
    with Contest() as contest:
        if name not in contest['users']:
            contest['users'][name] = {'password': pwd, 'name': name}
            status = True
    log(status, 'for registring {} {}'.format(name, pwd))
    return status


def is_logged_in(token):
    status = False
    with Contest() as contest:
        if token in contest['tokens']:
            status = True
    return status


def get_user(token):
    user = None
    with Contest() as contest:
        if token in contest['tokens']:
            user = contest['users'][contest['tokens'][token]]
    return user


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Contest management
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


def add_attempt_to_contest(attempt):
    log(attempt)
    attemptid = attempt['attempt_id']
    with Contest() as contest:
        attempt['stamp'] = str(time.time())
        contest['attempts'][attemptid] = attempt


def attempt_is_ok(qpk, lang, code):
    with Contest() as contest:
        if qpk in contest['questions']:
            if lang in contest['wrappers']:
                return True
    return False


def get_question_io(qpk):
    i, o = [], []
    with Contest() as contest:
        if qpk in contest['questions']:
            for k, v in contest['questions'][qpk]['testcases'].items():
                i.append(v['in'])
                o.append(v['out'])
    return i, o


def get_wrap(lang):
    wrap = None
    with Contest() as contest:
        if lang in contest['wrappers']:
            wrap = contest['wrappers'][lang]
    return wrap


def get_user_score(user):
    score = 0
    with Contest() as contest:
        if user in contest['users']:
            all_attempts = list(contest['attempts'].values())
            all_attempts = list(sorted(all_attempts,
                                       key=lambda x: float(x['stamp'])))
            q_cor = defaultdict(int)
            q_tot = defaultdict(int)
            u_q_seen = defaultdict(set)
            for A in all_attempts:
                a_user, q = A['user']['name'], A['qpk']
                q_tot[q] += 1
                if all(A['status']):
                    if q not in u_q_seen[a_user]:
                        # Valid attempt
                        u_q_seen[a_user].add(q)
                        if a_user == user:
                            q_cor[q] += 1
                            correct, total = q_cor[q], q_tot[q]
                            frac = float(total - correct) / total
                            # First attempt correct
                            elite_attempt = (total == 1 and correct == 1)
                            score += 1 if elite_attempt else frac
    return score


def get_all_users():
    with Contest() as contest:
        users = list(contest['users'].keys())
    return users
