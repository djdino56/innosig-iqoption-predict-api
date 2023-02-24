class BaseRoute:
    name = ""
    controller = None

    def __init__(self, app):
        self.app = app
        self.initiate()

    def initiate(self):
        self.app.add_url_rule('/{}'.format(self.__class__.name), 'create_{}'.format(self.__class__.name),
                              view_func=self.__class__.create, methods=['POST'])
        self.app.add_url_rule('/{}'.format(self.__class__.name), 'update_{}'.format(self.__class__.name),
                              view_func=self.__class__.update, methods=['PUT'])
        self.app.add_url_rule('/{}'.format(self.__class__.name), 'delete_{}'.format(self.__class__.name),
                              view_func=self.__class__.delete, methods=['DELETE'])
        self.app.add_url_rule('/{}'.format(self.__class__.name), 'get_{}'.format(self.__class__.name),
                              view_func=self.__class__.get, methods=['GET'])

    @classmethod
    def create(cls):
        pass

    @classmethod
    def get(cls):
        pass

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    def add_route(self, path, func, name, methods=None):
        if methods is None:
            methods = []
        self.app.add_url_rule(path, name, func, methods=methods)
