import asyncio
from pathlib import Path
from typing import Any

from aiohttp import web

from .routes import init_routes
from .views import SiteHandler

from .worker import initDB

path = Path(__file__).parent

async def init_app() -> web.Application:
    app = web.Application()
    initDB()
    handler = SiteHandler()
    init_routes(app, handler)
    return app


def main(args: Any = None) -> None:
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, host='127.0.0.1', port=8000)
