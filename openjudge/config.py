import os


static_root = os.path.join(os.getcwd(), 'staticroot')
variable_root = os.path.join(os.getcwd(), 'ContestData')
template_root = os.path.join(os.getcwd(), 'templatesroot')
working_root = os.path.join(os.getcwd(), 'workspace')


if not os.path.exists(static_root):
    os.mkdir(static_root)
if not os.path.exists(variable_root):
    os.mkdir(variable_root)
if not os.path.exists(template_root):
    os.mkdir(template_root)
if not os.path.exists(working_root):
    os.mkdir(working_root)
