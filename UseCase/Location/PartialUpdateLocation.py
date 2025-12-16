from Model.Location import Location
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class PartialUpdateLocation:

    locationRepo = None

    def __init__(self, repository):
        self.locationRepo = repository

    def do(self, locationId, data):
        location = self.locationRepo.findOne(locationId)
        if not location:
            raise NotFoundException
        Location.validateUpdateableValues(data)

        for key, value in data.items():
            location[key] = value

        return self.locationRepo.updateLocation(location)