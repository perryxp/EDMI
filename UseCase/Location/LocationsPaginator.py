from Service.Paginator import Paginator

class LocationsPaginator:    
    locationRepo = None

    def __init__(self, locationRepo):
        self.locationRepo = locationRepo

    def paginate(self, page, limit, filter = {}):
        count = self.locationRepo.count(filter)
        locations = self.locationRepo.find(page, limit, filter)
        return Paginator.paginate(locations, count, page, limit)
