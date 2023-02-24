from flask import request

from controllers.home import HomeController
from routes.base_route import BaseRoute


class HomeRoute(BaseRoute):
    name = "welcome"
    controller = HomeController()

    @classmethod
    def get(cls):
        return cls.controller.get(request)
