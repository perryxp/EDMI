from Model.Episode import Episode
from UseCase.AddCharacterEpisode import AddCharacterEpisode
from pprint import pprint


class AddEpisodeCharacter:

    episodeRepo = None
    characterRepo = None
    addCharacterEpisode = None
    dbManager = None

    def __init__(self, episodeRepo, characterRepo, addCharacterEpisode, dbManager):
        self.episodeRepo = episodeRepo
        self.characterRepo = characterRepo
        self.addCharacterEpisode = addCharacterEpisode
        self.dbManager = dbManager

    def do(self, episode, character):
        data = {'id': character['id'], 'name': character['name']}

        # with self.dbManager.transaction() as session:
        if 'characters' not in episode:
            episode['characters'] = []
        if not data in episode['characters']:
            episode['characters'].append(data)
            # self.addCharacterEpisode.do(episode, character)
        return self.episodeRepo.updateEpisode(episode['id'], episode)