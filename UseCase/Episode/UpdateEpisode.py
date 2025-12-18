from Model.Episode import Episode
from Exception.NotFoundException import NotFoundException
from pprint import pprint


class UpdateEpisode:

    episodeRepo = None

    def __init__(self, repository):
        self.episodeRepo = repository

    def do(self, id, data):
        create = False
        episode = self.episodeRepo.findOne(id)
        if not episode:
            create = True
        episode = Episode.create(data)
        episode['id'] = id
        return self.episodeRepo.addEpisode(episode, id) if create else self.episodeRepo.updateEpisode(episode)