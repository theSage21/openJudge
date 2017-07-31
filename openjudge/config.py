import os


timeout = 10  # Seconds
static_root = os.path.join(os.getcwd(), 'staticroot')
variable_root = os.path.join(os.getcwd(), 'ContestData')
template_root = os.path.join(os.getcwd(), 'templatesroot')
working_root = os.path.join(os.getcwd(), 'workspace')
log_root = os.path.join(os.getcwd(), 'logs')

valid_static = ['normalize.css', 'skeleton.css', 'main.js',
                'main.css', 'jquery.js']
valid_templates = ['home.html', 'analytics.html']
analysis_files = {'traffic': 'traffic.png',
                  'questions': 'question.png'}
plotscale = 10


if not os.path.exists(static_root):
    os.mkdir(static_root)
if not os.path.exists(variable_root):
    os.mkdir(variable_root)
if not os.path.exists(template_root):
    os.mkdir(template_root)
if not os.path.exists(working_root):
    os.mkdir(working_root)

n_threads_to_check_threads = 4
code_checking_threads = {}


default_contest = {'questions': {},
                   'intro': '',
                   'wrappers': {},
                   'attempts': {},
                   'tokens': {},
                   'users': {}
                   }
contest_json = 'contest.json'
