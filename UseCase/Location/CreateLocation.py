from Model.Location import Location

class CreateLocation:

    locationRepo = None

    def __init__(self, repository):
        self.locationRepo = repository

    def do(self, data):
        location = Location.create(data)
        return self.locationRepo.addLocation(location)
