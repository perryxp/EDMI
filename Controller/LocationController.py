from flask import Blueprint, jsonify, request
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
    def postLocation():
        data = request.json
        try:
            location = container.get('createLocation').do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(location)

    
    @bp.put('/locations/<int:id>')
    def putLocation(id):        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        location = locationRepo.findOne(id)
        if not location:
            return jsonify({'error': 'Not found'}), 404        
        
        try:
            location = container.get('updateLocation').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(location)
    
    @bp.patch('/locations/<int:id>')
    def patchLocation(id):
        data = request.json

        if not data:
            return jsonify({'error':  'Invalid JSON data'}), 400
        
        location = locationRepo.findOne(id)
        if not location:
            return jsonify({'error': 'Not found'}), 404
        
        updated = container.get('partialUpdateLocation').do(location, data)
        return jsonify(updated)
        
        
    @bp.delete('/locations/<int:id>')
    def deleteLocation(id):
        location = locationRepo.findOne(id)
        if not location:
            return jsonify({'error': 'Not found'}), 404
        
        locationRepo.deleteLocation(id)
        return [], 204
    
    
    @bp.post('locations/<int:id>/residents')
    def postLocationResidents(id):
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not data['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400
        
        location = locationRepo.findOne(id)
        resident = container.get('characterRepository').findOne(int(data['id']))

        if not location or not resident:
            return jsonify({'error': 'Not found'}), 404

        try:
            location = container.get('addLocationResident').do(location, resident)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return location
    

    @bp.delete('locations/<int:locationId>/residents/<int:characterId>')
    def delLocationResident(locationId, characterId):
        location = locationRepo.findOne(locationId)

        if not location or not location['residents']:
            return jsonify({'error': 'Not found'}), 404
        try:
            location = container.get('deleteLocationResident').do(location, characterId)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify(location)


    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({'error': str(e)}), 500

    return bp
