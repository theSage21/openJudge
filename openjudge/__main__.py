from . import server
from aiohttp import web

web.run_app(server.app)
