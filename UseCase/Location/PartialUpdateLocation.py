from Model.Location import Location
from pprint import pprint


class PartialUpdateLocation:

    locateRepo = None

    def __init__(self, repository):
        self.locateRepo = repository

    def do(self, location, data):
        Location.validateUpdateableValues(data)

        updateable = Location.create(location)
        for key, value in data.items():
            setattr(updateable, key, value)
        updateable.id = location['id']

        return self.locateRepo.updateLocation(location['id'], updateable)