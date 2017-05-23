import os
import bottle
import pkgutil
from shutil import copyfile
from openjudge import config

__all__ = ['log', 'section', 'render', 'setup_contest']


def log(*args):
    print(*args)


def section(text):
    log('='*70)
    log('.'*25, text)
    log('='*70)


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
    for template in ['normalize.css', 'skeleton.css']:
        with open(os.path.join(config.template_root, template), 'w') as fl:
            html = pkgutil.get_data('openjudge',
                                    'static/' + template).decode()
            fl.write(html)
        log('Copied {}'.format(template))


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


def setup_contest():
    "Set up the contest"
    __copy_intro__()
    __copy_templates__()
    __copy_static__()
    __copy_questions__()
