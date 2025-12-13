from Model.Episode import Episode
from pprint import pprint


class UpdateEpisode:

    episodeRepo = None

    def __init__(self, repository):
        self.episodeRepo = repository

    def do(self, id, data):
        episode = Episode.create(data)
        return self.episodeRepo.updateEpisode(id, episode)