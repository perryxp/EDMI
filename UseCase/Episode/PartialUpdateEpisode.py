from Model.Episode import Episode
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class PartialUpdateEpisode:

    episodeRepo = None

    def __init__(self, repository):
        self.episodeRepo = repository

    def do(self, id, data):
        episode = self.episodeRepo.findOne(id)
        if not episode:
            raise NotFoundException()
        
        Episode.validateUpdateableValues(data)

        for key, value in data.items():
            episode[key] = value

        return self.episodeRepo.updateEpisode(episode)