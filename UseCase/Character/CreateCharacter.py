from Model.Character import Character
from Model.Location import Location
from Exception.NotFoundException import NotFoundException
from Exception.InvalidParameterException import InvalidParameterException
from pprint import pprint

class CreateCharacter:

    characterRepo = None
    locationRepo = None

    def __init__(self, characterRepo, locationRepo):
        self.characterRepo = characterRepo
        self.locationRepo = locationRepo

    def do(self, data):
        origin = self.locationRepo.findOne(data['origin'])
        if origin is None:
            raise ValueError('Value for "origin" not valid')
        data['origin'] = Location.getReferenceData(origin)
        character = Character.create(data)
        return self.characterRepo.addCharacter(character)
