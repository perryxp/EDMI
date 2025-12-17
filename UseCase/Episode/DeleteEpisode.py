from Exception.NotFoundException import NotFoundException
from Exception.ConflictException import ConflictException
from pprint import pprint

class DeleteEpisode:
    episodeRepo = None

    def __init__(self, episodeRepo):
        self.episodeRepo = episodeRepo

    def do(self, episodeId):
        episode = self.episodeRepo.findOne(episodeId)
        if not episode:
            raise NotFoundException()        
        self.episodeRepo.deleteEpisode(episodeId)