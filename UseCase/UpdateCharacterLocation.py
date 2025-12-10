from Model.Character import Character
from pprint import pprint


class UpdateCharacterLocation:

    characterRepo = None

    def __init__(self, repository):
        self.characterRepo = repository

    def do(self, character, location):
        character['location'] = {'id': location['id'], 'name': location['name']}
        return self.characterRepo.updateCharacter(character['id'], character)