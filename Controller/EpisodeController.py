from flask import Blueprint, jsonify, request
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
    def postEpisode():
        data = request.json
        try:
            episode = container.get('createEpisode').do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(episode)

    @bp.put('/episodes/<int:id>')
    def putEpisode(id):        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        episode = episodeRepo.findOne(id)
        if not episode:
            return jsonify({'error': 'Not found'}), 404        
        
        try:
            episode = container.get('updateEpisode').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(episode)
    
    @bp.patch('/episodes/<int:id>')
    def patchEpisode(id):
        data = request.json

        if not data:
            return jsonify({'error':  'Invalid JSON data'}), 400
        
        episode = episodeRepo.findOne(id)
        if not episode:
            return jsonify({'error': 'Not found'}), 404
        
        updated = container.get('partialUpdateEpisode').do(episode, data)
        return jsonify(updated)
        
        
    @bp.delete('/episodes/<int:id>')
    def deleteEpisode(id):
        episode = episodeRepo.findOne(id)
        if not episode:
            return jsonify({'error': 'Not found'}), 404
        
        episodeRepo.deleteEpisode(id)
        return [], 204
     
    @bp.post('episodes/<int:id>/characters')
    def postEpisodeCharacter(id):
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not data['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400
        
        episode = episodeRepo.findOne(id)
        character = container.get('characterRepository').findOne(int(data['id']))

        if not episode or not character:
            return jsonify({'error': 'Not found'}), 404

        try:
            episode = container.get('addEpisodeCharacter').do(episode, character)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return episode
    
    @bp.delete('episodes/<int:episodeId>/characters/<int:characterId>')
    def delEpisodeCharacter(episodeId, characterId):
        episode = episodeRepo.findOne(episodeId)

        if not episode or not episode['characters']:
            return jsonify({'error': 'Not found'}), 404
        try:
            episode = container.get('deleteEpisodeCharacter').do(episode, characterId)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify(episode)
    

    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({'error': str(e)}), 500

    return bp