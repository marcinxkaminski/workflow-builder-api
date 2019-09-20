from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web import Request
from inspect import signature
from ml.config import API

ALLOWED_METHODS = API.get('ALLOWED_METHODS', ['GET', 'HEAD', 'POST', 'PUT', 'PATCH' 'DELETE'])


class RestEndpoint:
    def __init__(self):
        self.methods = {}

        for method_name in ALLOWED_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())

        if not method or method not in ALLOWED_METHODS:
            raise HTTPMethodNotAllowed('', ALLOWED_METHODS)

        wanted_args = list(signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            raise HttpBadRequest('')

        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})
