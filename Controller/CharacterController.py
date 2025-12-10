from flask import Blueprint, jsonify, request
from Repository.CharacterRepository import CharacterRepository
from Service.CharacterService import CharacterService
from pprint import pprint


def create_character_blueprint(
        characterRepo, 
        createCharacter,
        updateCharacter,
        partialUpdateCharacter,
        locationRepo,
        updateCharacterLocation,
        addCharacterEpisode,
        episodeRepo,
        deleteCharacterEpisode,
    ):
   
    bp = Blueprint('characters', __name__)

    @bp.get('/characters')
    def getCharacters():
        return jsonify(characterRepo.getCharacters())
    

    @bp.get('/characters/<int:id>')
    def getCharacter(id):
        character = characterRepo.getCharacter(id)
        if not character:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(character)
    
    
    @bp.post('/characters')
    def postCharacter():
        data = request.json
        try:
            character = createCharacter.do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(character)

    
    @bp.put('/characters/<int:id>')
    def putCharacter(id):        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        character = characterRepo.getCharacter(id)
        if not character:
            return jsonify({'error': 'Not found'}), 404        
        
        try:
            character = updateCharacter.do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(character)
    
    @bp.patch('/characters/<int:id>')
    def patchCharacter(id):
        data = request.json

        if not data:
            return jsonify({'error':  'Invalid JSON data'}), 400
        
        character = characterRepo.getCharacter(id)
        if not character:
            return jsonify({'error': 'Not found'}), 404
        
        updated = partialUpdateCharacter.do(character, data)
        return jsonify(updated)
        
        
    @bp.delete('/characters/<int:id>')
    def deleteCharacter(id):
        character = characterRepo.getCharacter(id)
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
        
        character = characterRepo.getCharacter(id)
        location = locationRepo.findOne(int(data['id']))

        if not character or not location:
            return jsonify({'error': 'Not found'}), 404        
        
        try:
            character = updateCharacterLocation.do(character, location)
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
        
        character = characterRepo.getCharacter(id)
        episode = episodeRepo.findOne(int(data['id']))

        if not character or not episode:
            return jsonify({'error': 'Not found'}), 404

        try:
            character = addCharacterEpisode.do(character, episode)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return character
    

    @bp.delete('characters/<int:characterId>/episodes/<int:episodeId>')
    def delCharacterEpisode(characterId, episodeId):
        character = characterRepo.getCharacter(characterId)

        if not character or not character['episodes']:
            return jsonify({'error': 'Not found'}), 404
        try:
            character = deleteCharacterEpisode.do(character, episodeId)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify(character)


    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({'error': str(e)}), 500

    return bp
