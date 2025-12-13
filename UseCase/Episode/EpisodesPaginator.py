from Service.Paginator import Paginator

class EpisodesPaginator:    
    episodesRepo = None

    def __init__(self, episodesRepo):
        self.episodesRepo = episodesRepo

    def paginate(self, page, limit, filter = {}):
        count = self.episodesRepo.count(filter)
        episodes = self.episodesRepo.find(page, limit, filter)
        return Paginator.paginate(episodes, count, page, limit)
