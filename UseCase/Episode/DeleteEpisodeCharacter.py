from Exception.NotFoundException import NotFoundException
from Model.Character import Character
from Model.Episode import Episode
from pprint import pprint

class DeleteEpisodeCharacter:

    episodeRepo = None
    characterRepo = None

    def __init__(self, episodeRepo, characterRepo):
        self.episodeRepo = episodeRepo
        self.characterRepo = characterRepo

    def do(self, episodeId, characterId):
        character = self.characterRepo.findOne(characterId)
        episode = self.episodeRepo.findOne(episodeId)
        if not episode:
            raise NotFoundException(f'Episode {episodeId} not found')
        if not character:
            raise NotFoundException(f'Character {characterId} not found')

        for i, characterInfo in enumerate(episode['characters']):
            if characterInfo['id'] == characterId:
                del episode['characters'][i]
                episode = self.episodeRepo.updateEpisode(episode)
            return {'episode': episode, 'character': self.characterRepo.findOne(characterId)}
        # raise NotFoundException(f'Character {str(Character.getReferenceData(character))} is not related to episode {str(Episode.getReferenceData(episode))}')