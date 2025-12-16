from Exception.NotFoundException import NotFoundException

class DeleteEpisodeCharacter:

    episodeRepo = None
    characterRepo = None
    dbManager = None

    def __init__(self, episodeRepo, characterRepo, dbManager):
        self.episodeRepo = episodeRepo
        self.characterRepo = characterRepo
        self.dbManager = dbManager

    def __deleteCharacterFromEpisode(self, episode, character, session):
        for i, characterInfo in enumerate(episode['characters']):
            if characterInfo['id'] == character['id']:
                del episode['characters'][i]
                break
        return self.episodeRepo.updateEpisode(episode['id'], episode, session)
    
    def __deleteEpisodeFromCharacter(self, character, episode, session):
        for i, episodeInfo in enumerate(character['episodes']):
            if episodeInfo['id'] == episode['id']:
                del character['episodes'][i]
                break
        return self.characterRepo.updateCharacter(character, session)
    
    def do(self, episodeId, characterId):
        episode = self.episodeRepo.findOne(episodeId)
        character = self.characterRepo.findOne(characterId)

        if not episode or not character:
            raise NotFoundException()

        with self.dbManager.transaction() as session:
            episode = self.__deleteCharacterFromEpisode(episode, character, session)
            character = self.__deleteEpisodeFromCharacter(character, episode, session)
        
        return {'episode': episode, 'character': character}