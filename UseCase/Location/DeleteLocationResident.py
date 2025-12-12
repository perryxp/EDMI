from Model.Location import Location
from pprint import pprint


class DeleteLocationResident:

    locationRepo = None
    characterRepo = None

    def __init__(self, locationRepo, characterRepo):
        self.locationRepo = locationRepo
        self.characterRepo = characterRepo

    def do(self, location, characterId):
        for i, residentInfo in enumerate(location['residents']):
            if residentInfo['id'] == characterId:
                del location['residents'][i]
                break

        return self.locationRepo.updateLocation(location['id'], location)