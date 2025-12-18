from flask import Blueprint, jsonify, request
from Exception.NotFoundException import NotFoundException
from Exception.InvalidParameterException import InvalidParameterException
from werkzeug.exceptions import HTTPException
from Security.Decorator import requireApikey
from pprint import pprint

def create_character_blueprint(container):
    characterRepo = container.get('characterRepository')   
    bp = Blueprint('characters', __name__)

    # @bp.before_request
    # def secure_blueprint():
    #     container.get('securityService').authorize(request)

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
    @requireApikey
    def postCharacter():
        data = request.json
        try:
            character = container.get('createCharacter').do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify(character), 201

    
    @bp.put('/characters/<int:id>')
    @requireApikey
    def putCharacter(id):        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400       
        
        try:
            character = container.get('updateCharacter').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        
        return jsonify(character)
    
    @bp.patch('/characters/<int:id>')
    @requireApikey
    def patchCharacter(id):
        data = request.json
        if not data:
            return jsonify({'error':  'Invalid JSON data'}), 400

        try:
            character = container.get('partialUpdateCharacter').do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        
        return jsonify(character)
        
        
    @bp.delete('/characters/<int:id>')
    @requireApikey
    def deleteCharacter(id):
        try:
            container.get('deleteCharacter').do(id)
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        return [], 204
    

    @bp.put('characters/<int:id>/location')
    @requireApikey
    def putCharacterLocation(id):
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not data['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400
        
        try:
            character = container.get('updateCharacterLocation').do(id, int(data['id']))
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        
        return jsonify(character)
    

    @bp.post('characters/<int:characterId>/episodes')
    @requireApikey
    def postCharacterEpisodes(characterId):
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        if not data['id']:
            return jsonify({'error': 'Missing required value "id"'}), 400

        try:
            episode = container.get('addEpisodeCharacter').do(int(data['id']), characterId)['character']
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        
        return jsonify(episode)
    

    @bp.delete('characters/<int:characterId>/episodes/<int:episodeId>')
    @requireApikey
    def delCharacterEpisode(characterId, episodeId):
        try:
            character = container.get('deleteEpisodeCharacter').do(episodeId, characterId)['character']
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
        # return [], 204
        return jsonify(character)


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
