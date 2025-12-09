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
        data = request.json

        if not data or 'name' not in data:
            return jsonify({"error": "Invalid data"}), 400
        
        character = CharacterService.createCharacter(data)
        repo.addCharacter(character)
        return repo.getCharacter(character.id)

    
    @bp.put("/characters/<int:id>")
    def putCharacter(id):
        data = request.json

        if not data or 'name' not in data:
            return jsonify({"error": "Invalid data"}), 400
               
        character = CharacterService.createCharacter(data)
        if not character:
            return jsonify({"error": "not found"}), 404
        
        repo.updateCharacter(id, character)

        return repo.getCharacter(id)
    
    @bp.patch("/characters/<int:id>")
    def patchCharacter(id):
        data = request.json

        if not data:
            return jsonify({"error": "Invalid data"}), 400
        
        character = repo.getCharacter(id)
        if not character:
            return jsonify({"error": "not found"}), 404
        
        CharacterService.validateUpdateableValues(data)

        editable = CharacterService.createCharacter(character)
        for key, value in data.items():
            setattr(editable, key, value)
        editable.id = id

        repo.updateCharacter(id, editable)
        return repo.getCharacter(id)
        
        
    @bp.delete("/characters/<int:id>")
    def deleteCharacter(id):
        repo.deleteCharacter(id)
        return [], 204

    @bp.errorhandler(Exception)
    def handle_error(e):
        return jsonify({"error": str(e)}), 500

    return bp
