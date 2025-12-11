from flask import Blueprint, jsonify, request
from pprint import pprint

def create_character_blueprint(container):
    characterRepo = container.get("characterRepository")   
    bp = Blueprint('characters', __name__)

    @bp.get('/characters')
    def getCharacters():
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
            if page <= 0 or limit <= 0:
                raise Exception('Page and limit must be integers greater than 0')
        except Exception as e:
            return jsonify({'error': 'Page and limit must be integers greater than 0'}), 400

        return jsonify(container.get('characterPaginator').paginate(int(page), int(limit)))

    
    @bp.get('/characters/<int:id>')
    def getCharacter(id):
        character = characterRepo.findOne(id)
        if not character:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(character)
    
    
    @bp.post('/characters')
    def postCharacter():
        data = request.json
        try:
            character = container.get('createCharacter').do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(character)

    
    @bp.put('/characters/<int:id>')
    def putCharacter(id):        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        character = characterRepo.findOne(id)
        if not character:
            return jsonify({'error': 'Not found'}), 404        
        
        try:
            character = container.get('updateCharacter').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(character)
    
    @bp.patch('/characters/<int:id>')
    def patchCharacter(id):
        data = request.json

        if not data:
            return jsonify({'error':  'Invalid JSON data'}), 400
        
        character = characterRepo.findOne(id)
        if not character:
            return jsonify({'error': 'Not found'}), 404
        
        updated = container.get('partialUpdateCharacter').do(character, data)
        return jsonify(updated)
        
        
    @bp.delete('/characters/<int:id>')
    def deleteCharacter(id):
        character = characterRepo.findOne(id)
        if not character:
            return jsonify({'error': 'Not found'}), 404
        
        characterRepo.deleteCharacter(id)
        return [], 204
    

    @bp.put('characters/<int:id>/location')
    def putCharacterLocation(id):
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not data['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400
        
        character = characterRepo.findOne(id)
        location = container.get('locationRepository').findOne(int(data['id']))

        if not character or not location:
            return jsonify({'error': 'Not found'}), 404        
        
        try:
            character = container.get('updateCharacterLocation').do(character, location)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(character)
    

    @bp.post('characters/<int:id>/episodes')
    def postCharacterEpisodes(id):
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not data['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400
        
        character = characterRepo.findOne(id)
        episode = container.get('episodeRepository').findOne(int(data['id']))

        if not character or not episode:
            return jsonify({'error': 'Not found'}), 404

        try:
            character = container.get('addCharacterEpisode').do(character, episode)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return character
    

    @bp.delete('characters/<int:characterId>/episodes/<int:episodeId>')
    def delCharacterEpisode(characterId, episodeId):
        character = characterRepo.findOne(characterId)

        if not character or not character['episodes']:
            return jsonify({'error': 'Not found'}), 404
        try:
            character = container.get('deleteCharacterEpisode').do(character, episodeId)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify(character)


    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({'error': str(e)}), 500

    return bp
