from Model.Location import Location
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class UpdateLocation:

    locationRepo = None

    def __init__(self, repository):
        self.locationRepo = repository

    def do(self, id, data):
        location = self.locationRepo.findOne(id)
        if not location:
            raise NotFoundException
        location = Location.create(data)
        location['id'] = id
        return self.locationRepo.updateLocation(location)