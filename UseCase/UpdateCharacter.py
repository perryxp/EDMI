from Model.Character import Character
from pprint import pprint


class UpdateCharacter:

    characterRepo = None

    def __init__(self, repository):
        self.characterRepo = repository

    def do(self, id, data):
        character = Character.create(data)
        return self.characterRepo.updateCharacter(id, character)