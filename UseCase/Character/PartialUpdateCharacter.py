from Model.Character import Character
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class PartialUpdateCharacter:

    characterRepo = None

    def __init__(self, repository):
        self.characterRepo = repository

    def do(self, characterId, data):
        character = self.characterRepo.findOne(characterId)
        if not character:
            raise NotFoundException()
        
        Character.validateUpdateableValues(data)
        for key, value in data.items():
            character[key] = value

        return self.characterRepo.updateCharacter(character)