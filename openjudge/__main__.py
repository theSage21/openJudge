import argparse
import logging

stdio_handler = logging.StreamHandler()
stdio_handler.setLevel(logging.INFO)
_logger = logging.getLogger("aiohttp.access")
_logger.addHandler(stdio_handler)
_logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--runner", default=False, action="store_true", help="Run runner instead of server"
)
parser.add_argument(
    "--endpoint",
    default="http://localhost:8080",
    type=str,
    help="Where should the runner register and get jobs from?",
)
parser.add_argument("--workdir", default="workdir", type=str, help="Working directory")

args = parser.parse_args()
if args.runner:
    from . import runner
    import pathlib

    runner.run(args.endpoint, pathlib.Path(args.workdir))
else:
    from . import server
    from aiohttp import web

    web.run_app(server.app())
