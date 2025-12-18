from flask import Blueprint, jsonify, request
from Exception.NotFoundException import NotFoundException
from Exception.ConflictException import ConflictException
from werkzeug.exceptions import HTTPException
from Security.Decorator import requireApikey
from pprint import pprint

def create_episode_blueprint(container):
    episodeRepo = container.get("episodeRepository")   
    bp = Blueprint('episode', __name__)

    @bp.get('/episodes')
    def getEpisodes():
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
            if page <= 0 or limit <= 0:
                raise Exception('Page and limit must be integers greater than 0')
        except Exception as e:
            return jsonify({'error': 'Page and limit must be integers greater than 0'}), 400

        return jsonify(container.get('episodesPaginator').paginate(int(page), int(limit)))
    
    @bp.get('/episodes/<int:id>')
    def getEpisode(id):
        episode = episodeRepo.findOne(id)
        if not episode:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(episode)
    
    @bp.post('/episodes')
    @requireApikey
    def postEpisode():
        data = request.json
        try:
            episode = container.get('createEpisode').do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(episode), 201

    @bp.put('/episodes/<int:id>')
    @requireApikey
    def putEpisode(id):        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        try:
            episode = container.get('updateEpisode').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        return jsonify(episode)
    
    @bp.patch('/episodes/<int:id>')
    @requireApikey
    def patchEpisode(id):
        data = request.json
        if not data:
            return jsonify({'error':  'Invalid JSON data'}), 400
        try:
            episode = container.get('partialUpdateEpisode').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        return jsonify(episode)
        
        
    @bp.delete('/episodes/<int:id>')
    @requireApikey
    def deleteEpisode(id):
        try:
            container.get('deleteEpisode').do(id)
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        except ConflictException as e:
            return jsonify({'error': str(e)}), 409
        return [], 204
     
    @bp.post('episodes/<int:episodeId>/characters')
    @requireApikey
    def postEpisodeCharacter(episodeId):
        characterData = request.json
        if not characterData:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not characterData['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400

        try:
            episode = container.get('addEpisodeCharacter').do(episodeId, int(characterData['id']))['episode']
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        
        return jsonify(episode), 201
    
    @bp.delete('episodes/<int:episodeId>/characters/<int:characterId>')
    @requireApikey
    def delEpisodeCharacter(episodeId, characterId):
        try:
            character = container.get('deleteEpisodeCharacter').do(episodeId, characterId)['episode']
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        return jsonify(character)
    
    @bp.post('episodes/<int:episodeId>/locations')
    @requireApikey
    def postEpisodeLocations(episodeId):
        locationData = request.json
        if not locationData:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not locationData['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400

        try:
            episode = container.get('addEpisodeLocation').do(episodeId, int(locationData['id']))['episode']
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        
        return jsonify(episode), 201
    
    @bp.delete('episodes/<int:episodeId>/locations/<int:locationId>')
    @requireApikey
    def delEpisodeLocation(episodeId, locationId):
        try:
            episode = container.get('deleteEpisodeLocation').do(episodeId, locationId)['episode']
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        return jsonify(episode)
    

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