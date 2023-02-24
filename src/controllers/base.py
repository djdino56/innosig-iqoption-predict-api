from flask import jsonify


class Base:

    @classmethod
    def create(cls, request):
        return
        pass

    @classmethod
    def update(cls, request):
        pass

    @classmethod
    def delete(cls, request):
        pass

    @classmethod
    def get(cls, request):
        pass


class JsonResponse:

    @staticmethod
    def success(data=None):
        response = {
            'code': 200,
            'status': 'success',
            'data': data
        }

        return jsonify(response), 200

    @staticmethod
    def not_found(data=None):
        if data is None:
            data = 'Resource Not Found'

        response = {
            'code': 404,
            'status': 'error',
            'data': data,
            'message': 'not_found'
        }

        return jsonify(response), 404

    @staticmethod
    def delete(data=None):
        if data is None:
            data = 'Resource Deleted'

        response = {
            'code': 200,
            'status': 'success',
            'data': data,
            'message': 'resource_deleted'
        }
        return jsonify(response), 200

    @staticmethod
    def invalid_response(data=None):
        if data is None:
            data = 'Invalid Data'

        response = {
            'code': 400,
            'status': 'error',
            'data': data,
            'message': 'invalid_data'
        }
        return jsonify(response), 400

    @staticmethod
    def error_response(data, response_code=422):

        response = {
            'code': response_code,
            'status': 'error',
            'data': data,
            'message': 'unprocessable_entity'
        }
        return jsonify(response), response_code
