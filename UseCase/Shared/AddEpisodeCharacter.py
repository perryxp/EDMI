from Model.Character import Character
from Model.Episode import Episode
from Exception.NotFoundException import NotFoundException
from pprint import pprint

class AddEpisodeCharacter:

    episodeRepo = None
    characterRepo = None
    dbManager = None

    def __init__(self, episodeRepo, characterRepo, dbManager):
        self.episodeRepo = episodeRepo
        self.characterRepo = characterRepo
        self.dbManager = dbManager

    def __addCharacterToEpisode(self, episode, character, session):
        characterData = Character.getReferenceData(character)
        if 'characters' not in episode:
            episode['characters'] = []
        if not characterData in episode['characters']:
            episode['characters'].append(characterData)
        return self.episodeRepo.updateEpisode(episode['id'], episode, session)


    def __addEpisodeToCharacter(self, character, episode, session):
        episodeData = Episode.getReferenceData(episode)
        if 'episodes' not in character:
            character['episodes'] = []
        if not episodeData in character['episodes']:
            character['episodes'].append(episodeData)
        return self.characterRepo.updateCharacter(character, session)

        
    def do(self, episodeId, characterId):
        episode = self.episodeRepo.findOne(episodeId)
        character = self.characterRepo.findOne(characterId)

        if not episode or not character:
            raise NotFoundException()

        with self.dbManager.transaction() as session:
            episode = self.__addCharacterToEpisode(episode, character, session)
            character = self.__addEpisodeToCharacter(character, episode, session)
        
        return {'episode': episode, 'character': character}

