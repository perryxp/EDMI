from Model.Character import Character

class CreateCharacter:

    characterRepo = None

    def __init__(self, repository):
        self.characterRepo = repository

    def do(self, data):
        character = Character.create(data)
        return self.characterRepo.addCharacter(character)
