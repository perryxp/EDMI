from Exception.NotFoundException import NotFoundException

class DeleteEpisodeLocation:

    episodeRepo = None

    def __init__(self, episodeRepo):
        self.episodeRepo = episodeRepo

    def do(self, episodeId, locationId):
        episode = self.episodeRepo.findOne(episodeId)
        if not episode:
            raise NotFoundException()
        for i, locationInfo in enumerate(episode['locations']):
            if locationInfo['id'] == locationId:
                del episode['locations'][i]
                break
        return self.episodeRepo.updateEpisode(episode)
