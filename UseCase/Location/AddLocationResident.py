from Model.Location import Location
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class AddLocationResident:

    locationRepo = None
    characterRepo = None

    def __init__(self, locationRepo, characterRepo):
        self.locationRepo = locationRepo
        self.characterRepo = characterRepo

    def do(self, locationId, residentId):
        location = self.locationRepo.findOne(locationId)
        resident = self.characterRepo.findOne(residentId)
        if not location or not resident:
            raise NotFoundException()
        data = {'id': resident['id'], 'name': resident['name']}
        if 'residents' not in location:
            location['residents'] = []
        if not data in location['residents']:
            location['residents'].append(data)
        return self.locationRepo.updateLocation(location)