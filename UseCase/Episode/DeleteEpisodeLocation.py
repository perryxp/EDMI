from Exception.NotFoundException import NotFoundException
from Model.Location import Location
from Model.Episode import Episode

class DeleteEpisodeLocation:

    episodeRepo = None
    locationRepo = None

    def __init__(self, episodeRepo, locationRepo):
        self.episodeRepo = episodeRepo
        self.locationRepo = locationRepo

    def do(self, episodeId, locationId):
        episode = self.episodeRepo.findOne(episodeId)
        location = self.locationRepo.findOne(locationId)
        if not episode:
            raise NotFoundException(f'Episode {episodeId} not found')
        if not location:
            raise NotFoundException(f'Character {locationId} not found')
        for i, locationInfo in enumerate(episode['locations']):
            if locationInfo['id'] == locationId:
                del episode['locations'][i]
                episode = self.episodeRepo.updateEpisode(episode)
                return {'episode': episode, 'location': self.locationRepo.findOne(locationId)}
        raise NotFoundException(f'Location {str(Location.getReferenceData(location))} is not related to episode {str(Episode.getReferenceData(episode))}')
