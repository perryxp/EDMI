from Model.Location import Location
from pprint import pprint


class AddLocationResident:

    locationRepo = None
    characterRepo = None

    def __init__(self, locationRepo, characterRepo):
        self.locationRepo = locationRepo
        self.characterRepo = characterRepo

    def do(self, location, resident):
        data = {'id': resident['id'], 'name': resident['name']}
        if 'residents' not in location:
            location['residents'] = []
        if not data in location['residents']:
            location['residents'].append(data)
        return self.locationRepo.updateLocation(location['id'], location)