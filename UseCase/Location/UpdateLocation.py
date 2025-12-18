from Model.Location import Location
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class UpdateLocation:

    locationRepo = None

    def __init__(self, repository):
        self.locationRepo = repository

    def do(self, id, data):
        create = False
        location = self.locationRepo.findOne(id)
        if not location:
            create = True
        location = Location.create(data)
        location['id'] = id
        return self.locationRepo.addLocation(location, id) if create else self.locationRepo.updateLocation(location)