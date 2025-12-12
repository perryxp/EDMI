from Model.Character import Character
from pprint import pprint


class AddCharacterEpisode:

    characterRepo = None
    episodeRepo = None

    def __init__(self, characterRepo, episodeRepo):
        self.characterRepo = characterRepo
        self.episodeRepo = episodeRepo

    def do(self, character, episode):
        data = {'id': episode['id'], 'name': episode['name'], 'episode': episode['episode']}
        if 'episodes' not in character:
            character['episodes'] = []
        if data not in character['episodes']:
            character['episodes'].append(data)
        return self.characterRepo.updateCharacter(character['id'], character)