from Exception.NotFoundException import NotFoundException
from Exception.ConflictException import ConflictException
from pprint import pprint

class DeleteEpisode:
    episodeRepo = None
    locationRepo = None
    dbManager = None

    def __init__(self, episodeRepo, locationRepo, dbManager):
        self.episodeRepo = episodeRepo
        self.locationRepo = locationRepo
        self.dbManager = dbManager

    def do(self, episodeId):
        episode = self.episodeRepo.findOne(episodeId)
        if not episode:
            raise NotFoundException()        
        self.episodeRepo.deleteEpisode(episodeId)