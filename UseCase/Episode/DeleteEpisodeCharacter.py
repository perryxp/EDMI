from Model.Character import Character
from pprint import pprint


class DeleteEpisodeCharacter:

    episodeRepo = None
    characterRepo = None
    dbManager = None
    deleteCharacterEpisode = None

    def __init__(self, episodeRepo, characterRepo, deleteCharacterEpisode, dbManager):
        self.episodeRepo = episodeRepo
        self.characterRepo = characterRepo
        self.deleteCharacterEpisode
        self.dbManager = dbManager

    def do(self, episode, characterId):
        for i, episodeInfo in enumerate(episode['characters']):
            if episodeInfo['id'] == characterId:
                del episode['characters'][i]
                break

        return self.episodeRepo.updateEpisode(episode['id'], episode)