import os
import bottle
import pkgutil
from shutil import copyfile
from openjudge import config

__all__ = ['log', 'section', 'render', 'update_contest_data']


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
    log('Intro copied into static files')


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


def update_contest_data():
    __copy_intro__()
    __copy_templates__()
    __copy_static__()
