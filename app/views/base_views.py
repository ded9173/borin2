from flask import jsonify
from flask.views import MethodView

class BaseAPIView(MethodView):

    decorators = []

    def _success(self, data, status=200):
        return jsonify(data), status
    def error_response(self, message, status=400):
        return jsonify({'error': 'error', 'massage': message}), status

    def _not_found_response(self, resource='Ресурс'):
        return jsonify({'error': 'not found', 'massage': f'{resource} не найден'}), 404