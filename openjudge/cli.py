import sys
from openjudge import tools
from openjudge.interface import app


def main():
    if sys.version_info < (3, 5):
        raise Exception('You require Python3.5 or above to run OpenJudge')
    print('openjudge <interface> <port>')
    ip, port = '0.0.0.0', 8080
    try:
        ip = sys.argv[1]
    except IndexError:
        pass
    else:
        try:
            port = sys.argv[2]
        except IndexError:
            pass
    tools.section('Setting Up Openjudge')
    tools.setup_contest()
    tools.section('Starting Webserver')
    app.run(server='paste', host=ip, port=port)
