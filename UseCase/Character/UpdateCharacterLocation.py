from Model.Character import Character
from Model.Location import Location
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class UpdateCharacterLocation:

    characterRepo = None
    locationRepo = None

    def __init__(self, characterRepo, locationRepo):
        self.characterRepo = characterRepo
        self.locationRepo = locationRepo

    def do(self, characterId, locationId):
        character = self.characterRepo.findOne(characterId)
        location = self.locationRepo.findOne(locationId)

        if not character or not location:
            raise NotFoundException()
        
        character['location'] = Location.getReferenceData(location)
        return self.characterRepo.updateCharacter(character)