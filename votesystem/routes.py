import pathlib
from aiohttp import web
from .views import SiteHandler

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application, handler: SiteHandler) -> None:
    add_route = app.router.add_route

    add_route('GET', '/', handler.index, name='index')
    add_route('GET', '/results', handler.results, name='results')
    add_route('POST', '/addVotes', handler.addVotes, name='addVotes')
    
    app.router.add_static(
        '/img/', path=(PROJECT_PATH / 'img'), name='img'
    )
		
    app.router.add_static(
        '/db/', path=(PROJECT_PATH / 'db'), name='db'
    )


