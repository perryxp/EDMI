from flask import Blueprint, jsonify, request
from Exception.NotFoundException import NotFoundException
from Exception.ConflictException import ConflictException
from werkzeug.exceptions import HTTPException
from Security.Decorator import requireApikey
from pprint import pprint

def create_location_blueprint(container):
    locationRepo = container.get("locationRepository")   
    bp = Blueprint('location', __name__)

    @bp.get('/locations')
    def getLocations():
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
            if page <= 0 or limit <= 0:
                raise Exception('Page and limit must be integers greater than 0')
        except Exception as e:
            return jsonify({'error': 'Page and limit must be integers greater than 0'}), 400

        return jsonify(container.get('locationsPaginator').paginate(int(page), int(limit)))

    
    @bp.get('/locations/<int:id>')
    def getLocation(id):
        location = locationRepo.findOne(id)
        if not location:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(location)
    
    
    @bp.post('/locations')
    @requireApikey
    def postLocation():
        data = request.json
        try:
            location = container.get('createLocation').do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(location), 201

    
    @bp.put('/locations/<int:id>')
    @requireApikey
    def putLocation(id):        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        try:
            location = container.get('updateLocation').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        
        return jsonify(location)
    
    @bp.patch('/locations/<int:id>')
    @requireApikey
    def patchLocation(id):
        data = request.json

        if not data:
            return jsonify({'error':  'Invalid JSON data'}), 400
        try:
            location = container.get('partialUpdateLocation').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        return jsonify(location)
        
        
    @bp.delete('/locations/<int:id>')
    @requireApikey
    def deleteLocation(id):
        try:
            container.get('deleteLocation').do(id)
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        except ConflictException as e:
            return jsonify({'error': str(e)}), 409
        return [], 204
    
    
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
