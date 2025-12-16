from Exception.NotFoundException import NotFoundException
from Exception.ConflictException import ConflictException
from pprint import pprint

class DeleteLocation:
    locationRepo = None

    def __init__(self, locationRepo):
        self.locationRepo = locationRepo

    def do(self, locationId):
        location = self.locationRepo.findOne(locationId)
        pprint(location)
        if not location:
            raise NotFoundException()
        if 'episodes' in location and len(location['episodes']) > 0:
            raise ConflictException(f'Location "{location['name']}" exists in episodes {str(location['episodes'])}')
        if 'residents' in location and len(location['residents']) > 0:
            raise ConflictException(f'Location "{location['name']}" has residents {str(location['residents'])}')
        self.locationRepo.deleteLocation(locationId)
        