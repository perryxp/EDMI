from Model.Character import Character
from pprint import pprint


class PartialUpdateCharacter:

    characterRepo = None

    def __init__(self, repository):
        self.characterRepo = repository

    def do(self, character, data):
        Character.validateUpdateableValues(data)

        updateable = Character.create(character)
        for key, value in data.items():
            setattr(updateable, key, value)
        updateable.id = character['id']

        return self.characterRepo.updateCharacter(character['id'], updateable)