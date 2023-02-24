from controllers.base import Base as BaseController, JsonResponse


class HomeController(BaseController):

    def __init__(self):
        pass

    @classmethod
    def get(cls, request):
        return JsonResponse.success('Jurrex API ({0}).'.format('development'))
