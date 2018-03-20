import os
import json
import asyncio
import argparse
from .server import run_server
from motor import motor_asyncio
from .utils import add_questions_from_dir
from .worker import run_judge
from .default_interface import copy_defaults


def get_db(uri):
    db_name = uri.split('/')[-1]
    client = motor_asyncio.AsyncIOMotorClient(uri)
    db = client[db_name]
    return db


def _add_questions(qdir, timeout, db):
    loop = asyncio.get_event_loop()
    todo = [asyncio.ensure_future(add_questions_from_dir(qdir, timeout, db))]
    loop.run_until_complete(asyncio.gather(*todo))


def main():
    mongo_uri = os.environ.get("MONGO_URI",
                               "mongodb://localhost:27017/openjudge")
    desc = 'Voody Ecommerce server library'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--server-host', action='store',
                        default='0.0.0.0',
                        help='What host to run the server on?')
    parser.add_argument('--server-port', action='store',
                        default=8000,
                        help='What port to run the server on?')
    parser.add_argument("--mongo-uri", action="store",
                        default=mongo_uri,
                        help='The MongoDB URI')
    parser.add_argument('--workspace', action='store',
                        default='workspace',
                        help='Folder to contain all working data')
    parser.add_argument('--template-dir', action='store',
                        default='templates',
                        help='Where are the templates stored?')
    parser.add_argument('--static-dir', action='store',
                        default='staticfiles',
                        help='Where are the static files stored?')
    parser.add_argument('--wrapmap', action='store',
                        default='wrappers.json',
                        help='Wrappers in JSON format')
    parser.add_argument('--add-questions-from', action='store',
                        default='questions',
                        help="Where to add questions from?")
    parser.add_argument('--timeout', action='store',
                        default=10,
                        help="How much total time does each attempt get?")
    parser.add_argument('--judge', action='store_true',
                        default=False,
                        help='Start the judge')
    parser.add_argument('--n-judges', action='store',
                        default=4, help='How many concurrent judges')
    args = parser.parse_args()
    copy_defaults(args.template_dir, args.static_dir, args.wrapmap)
    database = get_db(args.mongo_uri)
    if not os.path.exists(args.workspace):
        os.mkdir(args.workspace)

    with open(args.wrapmap, 'r') as fl:
        wrapmap = json.load(fl)

    if args.judge:
        run_judge(args.mongo_uri, args.n_judges)

    _add_questions(args.add_questions_from, args.timeout, database)
    # ------------------------------------------
    print('Initiating Server')
    run_server(args.server_port, args.server_host,
               database,
               args.static_dir,
               wrapmap,
               args.workspace,
               args.template_dir)
