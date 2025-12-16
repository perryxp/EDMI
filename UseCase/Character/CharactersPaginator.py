from Service.Paginator import Paginator

class CharactersPaginator:    
    characterRepo = None

    def __init__(self, characterRepo):
        self.characterRepo = characterRepo

    def paginate(self, page, limit, filter = {}):
        count = self.characterRepo.count(filter)
        characters = self.characterRepo.find(page, limit, filter)
        return Paginator.paginate(characters, count, page, limit)
