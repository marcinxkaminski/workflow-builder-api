from aiohttp import web
from ml.cleaner import run as run_cleaner
from ml.interface import setup as setup_interface

app = web.Application()
setup_interface(router=app.router)
web.run_app(app)
run_cleaner()
