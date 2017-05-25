import sys
from openjudge import tools
from openjudge.interface import app


def main():
    if sys.version_info < (3, 5):
        raise Exception('You require Python3.5 or above to run OpenJudge')
    tools.section('Setting Up Openjudge')
    tools.setup_contest()
    tools.section('Starting Webserver')
    app.run(server='paste')
