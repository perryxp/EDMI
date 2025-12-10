from Model.Character import Character
from pprint import pprint


class DeleteCharacterEpisode:

    characterRepo = None
    episodeRepo = None

    def __init__(self, characterRepo, episodeRepo):
        self.characterRepo = characterRepo
        self.episodeRepo = episodeRepo

    def do(self, character, episodeId):
        for i, episodeInfo in enumerate(character['episodes']):
            if episodeInfo['id'] == episodeId:
                del character['episodes'][i]
                break

        return self.characterRepo.updateCharacter(character['id'], character)