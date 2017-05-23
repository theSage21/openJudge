import os
import bottle
from shutil import copyfile
from openjudge import config


def render(template, data=None):
    data = data if data is not None else dict()
    template_dir = config.template_root
    with open(os.path.join(template_dir, template)) as fl:
        html = fl.read()
    return bottle.template(html, **data)


def update_contest_data():
    intro = os.path.join(config.variable_root, 'intro.txt')
    if not os.path.exists(config.static_root):
        os.mkdir(config.static_root)
    intro_to = os.path.join(config.static_root, 'intro.txt')
    copyfile(intro, intro_to)
    # ---------------------------------
