from Model.Location import Location
from Model.Episode import Episode
from Exception.NotFoundException import NotFoundException
from pprint import pprint

class AddEpisodeLocation:

    episodeRepo = None
    locationRepo = None

    def __init__(self, episodeRepo, locationRepo):
        self.episodeRepo = episodeRepo
        self.locationRepo = locationRepo

    def do(self, episodeId, locationId):
        episode = self.episodeRepo.findOne(episodeId)
        location = self.locationRepo.findOne(locationId)

        if not episode or not location:
            raise NotFoundException()
        data = Location.getReferenceData(location)
        if not 'locations' in episode:
            episode['locations'] = []
        if not data in episode['locations']:
            episode['locations'].append(data)
        return self.episodeRepo.updateEpisode(episode)

