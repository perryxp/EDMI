from Model.Character import Character
from Model.Episode import Episode
from Exception.NotFoundException import NotFoundException
from pprint import pprint

class AddEpisodeCharacter:

    episodeRepo = None
    characterRepo = None

    def __init__(self, episodeRepo, characterRepo):
        self.episodeRepo = episodeRepo
        self.characterRepo = characterRepo

    def do(self, episodeId, characterId):
        episode = self.episodeRepo.findOne(episodeId)
        character = self.characterRepo.findOne(characterId)

        if not episode or not character:
            raise NotFoundException()

        data = Character.getReferenceData(character)
        if not 'characters' in episode:
            episode['characters'] = []
        if not data in episode['characters']:
            episode['characters'].append(data)
        episode = self.episodeRepo.updateEpisode(episode)
        
        return episode

