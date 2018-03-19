import os
import json
import argparse
from .server import run_server
from motor import motor_asyncio


def get_db(uri):
    db_name = uri.split('/')[-1]
    client = motor_asyncio.AsyncIOMotorClient(uri)
    db = client[db_name]
    return db


def main():
    mongo_uri = os.environ.get("MONGO_URI",
                               "mongodb://localhost:27017/exchange")
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
    args = parser.parse_args()
    database = get_db(args.mongo_uri)
    with open(args.wrapmap, 'r') as fl:
        wrapmap = json.load(fl)
    # ------------------------------------------
    print('Initiating Server')
    run_server(args.server_port, args.server_host,
               database,
               args.static_dir,
               wrapmap,
               args.workspace,
               args.templatedir)
