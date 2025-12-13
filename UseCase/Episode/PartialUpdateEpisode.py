from Model.Episode import Episode
from pprint import pprint


class PartialUpdateEpisode:

    episodeRepo = None

    def __init__(self, repository):
        self.episodeRepo = repository

    def do(self, episode, data):
        Episode.validateUpdateableValues(data)

        updateable = Episode.create(episode)
        for key, value in data.items():
            setattr(updateable, key, value)
        updateable.id = episode['id']

        return self.episodeRepo.updateEpisode(episode['id'], updateable)