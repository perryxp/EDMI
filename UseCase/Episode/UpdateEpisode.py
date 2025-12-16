from Model.Episode import Episode
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class UpdateEpisode:

    episodeRepo = None

    def __init__(self, repository):
        self.episodeRepo = repository

    def do(self, id, data):
        episode = self.episodeRepo.findOne(id)
        if not episode:
            raise NotFoundException()
        episode = Episode.create(data)
        episode['id'] = id
        return self.episodeRepo.updateEpisode(episode)