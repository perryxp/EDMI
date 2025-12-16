from Model.Episode import Episode
from pymongo import ReturnDocument

class EpisodeRepository:
    episodeCollection = None

    def __init__(self, db):
        self.episodeCollection = db.getCollection("rick&morty", "episodes")

    def findOne(self, id):
        return self.episodeCollection.find_one({'id': id}, {'_id': 0})

    def find(self, page, limit, filter = {}):
        skip = (page - 1) * limit
        result = self.episodeCollection.find(filter, {'_id': 0}).skip(skip).limit(limit)
        return list(result.sort([('id', 1)]))
    
    def count(self, filter = {}):
        return self.episodeCollection.count_documents(filter)
    
    def addEpisode(self, episode, session = None):
        id = self.__calculateNextId()
        episode.id = id
        self.episodeCollection.insert_one(
            episode.__dict__ if isinstance(episode, Episode) else episode
        )
        return self.findOne(episode.id)
    
    def updateEpisode(self, id, episode, session = None):

        if isinstance(episode, Episode):
            episode.id = id
        else:
            episode['id'] = id
        return self.episodeCollection.find_one_and_update(
            {'id': id},
            {'$set': episode.__dict__ if isinstance(episode, Episode) else episode},
            session = session,
            projection={"_id": 0},
            return_document=ReturnDocument.AFTER         
        )
    
    def deleteEpisode(self, id, session = None):
        return self.episodeCollection.delete_one({'id': id}, session = session)
    
    def __calculateNextId(self):
        result = self.episodeCollection.find_one({}, {'id': 1, '_id': 0},sort=[('id', -1)])
        
        return (result['id'] + 1) if result else 1