from Model.Location import Location
from pprint import pprint


class UpdateLocation:

    locationRepo = None

    def __init__(self, repository):
        self.locationRepo = repository

    def do(self, id, data):
        location = Location.create(data)
        return self.locationRepo.updateLocation(id, location)