from flask import Blueprint, jsonify, request, current_app
from Exception.NotFoundException import NotFoundException
from Exception.InvalidParameterException import InvalidParameterException
from werkzeug.exceptions import HTTPException
from pprint import pprint

def create_auth_blueprint(container):
    bp = Blueprint('auth', __name__)

    @bp.post('/auth')
    def postAuth():
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400 
        user = data.get('user', None)
        password = data.get('pass', None)

        if not user:
            return jsonify({'error': 'User info not found in request'}), 400
        if not password:
            return jsonify({'error': 'Password info not found in request'}), 400
       
        apikey = container.get('authService').authorize(user, password)
        return jsonify({'apikey': apikey})

    @bp.errorhandler(HTTPException)
    def handle_http_error(e):
        return jsonify({
            "error": e.name,
            "message": e.description
        }), e.code

    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({'error': str(e)}), 500

    return bp
