from flask import Blueprint, jsonify, request
from Repository.CharacterRepository import CharacterRepository
from Service.CharacterService import CharacterService
from pprint import pprint


def create_character_blueprint(
        characterRepo, 
        createCharacter,
        updateCharacter,
        partialUpdateCharacter
        ):
    bp = Blueprint("characters", __name__)

    @bp.get("/characters")
    def getCharacters():
        return jsonify(characterRepo.getCharacters())

    @bp.get("/characters/<int:id>")
    def getCharacter(id):
        character = characterRepo.getCharacter(id)
        if not character:
            return jsonify({"error": "not found"}), 404
        return jsonify(character)
    
    @bp.post("/characters")
    def postCharacter():
        data = request.json
        try:
            character = createCharacter.do(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(character)
    
        # character = CharacterService.createCharacter(data)
        # repo.addCharacter(character)
        # return repo.getCharacter(character.id)

    
    @bp.put("/characters/<int:id>")
    def putCharacter(id):
        character = characterRepo.getCharacter(id)
        if not character:
            return jsonify({"error": "not found"}), 404
        
        data = request.json
        if not data:
            return jsonify({"error": "Invalid data"}), 400
        
        try:
            character = updateCharacter.do(id, data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        return jsonify(character)
    
    @bp.patch("/characters/<int:id>")
    def patchCharacter(id):
        data = request.json

        if not data:
            return jsonify({"error": "Invalid data"}), 400
        
        character = characterRepo.getCharacter(id)
        if not character:
            return jsonify({"error": "not found"}), 404
        
        updated = partialUpdateCharacter.do(character, data)
        return jsonify(updated)
        
        
    @bp.delete("/characters/<int:id>")
    def deleteCharacter(id):
        repo.deleteCharacter(id)
        return [], 204

    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({"error": str(e)}), 500

    return bp
