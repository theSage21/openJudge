import os
import pkgutil


def __copy_template(templatedir):
    if not os.path.exists(templatedir):
        html = pkgutil.get_data('openjudge', 'templates/home.html')
        if html is not None:
            os.mkdir(templatedir)
            with open(os.path.join(templatedir, 'home.html'), 'w') as fl:
                fl.write(html.decode())


def __copy_static(staticdir):
    if not os.path.exists(staticdir):
        os.mkdir(staticdir)
        for st in ['Chart.min.js', 'jquery-3.2.1.min.js',
                   'js.cookie.min.js', 'main.css', 'main.js',
                   'showdown.min.js']:
            content = pkgutil.get_data('openjudge', 'staticfiles/'+st)
            if content is not None:
                with open(os.path.join(staticdir, st), 'w') as fl:
                    fl.write(content.decode())


def __copy_wrapper(wrapperfile):
    if not os.path.exists(wrapperfile):
        wrap = pkgutil.get_data('openjudge', 'wrappers.json')
        if wrap is not None:
            with open(wrapperfile, 'w') as fl:
                fl.write(wrap.decode())


def copy_defaults(tempdir, staticdir, wrapperfile):
    __copy_wrapper(wrapperfile)
    __copy_template(tempdir)
    __copy_static(staticdir)
