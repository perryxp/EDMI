from Model.Episode import Episode
from datetime import datetime

class CreateEpisode:

    episodeRepo = None

    def __init__(self, repository):
        self.episodeRepo = repository

    def do(self, data):
        try:
            date = datetime.strptime(data['air_date'], '%B %d, %Y').strftime("%B %d, %Y")
        except (TypeError, ValueError):
            raise ValueError('air_date must be like "' + datetime.now().strftime("%B %d, %Y") +'"')
        data['air_date'] = date
        episode = Episode.create(data)
        return self.episodeRepo.addEpisode(episode)
