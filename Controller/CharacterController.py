from flask import Blueprint, jsonify, request
from Repository.CharacterRepository import CharacterRepository
from Service.CharacterService import CharacterService
from pprint import pprint


def create_character_blueprint(db):
    repo = CharacterRepository(db)
    bp = Blueprint("characters", __name__)

    @bp.get("/characters")
    def getCharacters():
        return jsonify(repo.getCharacters())

    @bp.get("/characters/<int:id>")
    def getCharacter(id):
        character = repo.getCharacter(id)
        if not character:
            return jsonify({"error": "not found"}), 404
        return jsonify(character)
    
    @bp.post("/characters")
    def postCharacter():
        pprint('0000000000000')
        data = request.json

        if not data or 'name' not in data:
            return jsonify({"error": "Invalid data"}), 400
        
        # character = CharacterService.createCharacter(data)
        # CharacterRepository.addCharacter(character)
    
        pprint(data)
        return []
    
    @bp.put("/characters/<int:id>")
    def putCharacter(id):
        return repo.getCharacter(id)
        data = request.json

        if not data or 'name' not in data:
            return jsonify({"error": "Invalid data"}), 400
        
        # character = CharacterService.createCharacter(data)
        # CharacterRepository.updateCharacter(id, character)

        pprint(data)
        return repo.getCharacter(id)
    
    @bp.delete("/characters/<int:id>")
    def deleteCharacter(id):
        CharacterRepository.deleteCharacter(id)
        return [], 204

    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({"error": str(e)}), 500

    return bp
