class DeleteEpisodeCharacter:

    episodeRepo = None
    characterRepo = None
    dbManager = None
    deleteCharacterEpisode = None

    def __init__(self, episodeRepo, characterRepo, deleteCharacterEpisode, dbManager):
        self.episodeRepo = episodeRepo
        self.characterRepo = characterRepo
        self.deleteCharacterEpisode = deleteCharacterEpisode
        self.dbManager = dbManager

    def do(self, episode, characterId):
        with self.dbManager.transaction() as session:
            for i, episodeInfo in enumerate(episode['characters']):
                if episodeInfo['id'] == characterId:
                    del episode['characters'][i]
                    break
            character = self.characterRepo.findOne(characterId)
            self.deleteCharacterEpisode.do(character, episode['id'])
            return self.episodeRepo.updateEpisode(episode['id'], episode, session)