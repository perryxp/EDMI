from Model.Character import Character
from pymongo import ReturnDocument

class EpisodeRepository:
    episodeCollection = None

    def __init__(self, db):
        self.episodeCollection = db.getCollection("rick&morty", "episodes")

    def findOne(self, id):
        return self.episodeCollection.find_one({'id': id}, {'_id': 0})

    def findAll(self):
        return list(self.episodeCollection.find({}, {'_id': 0}))
    
    # def addCharacter(self, character):
    #     id = self.__calculateNextId()
    #     character.id = id
    #     self.characterCollection.insert_one(
    #         character.__dict__ if isinstance(character, Character) else character
    #     )
    #     return self.getCharacter(character.id)
    
    # def updateCharacter(self, id, character):
    #     character.id = id
    #     return self.characterCollection.find_one_and_update(
    #         {'id': id},
    #         {'$set': character.__dict__ if isinstance(character, Character) else character},
    #         projection={"_id": 0},
    #         return_document=ReturnDocument.AFTER         
    #     )
    
    # def deleteCharacter(self, id):
    #     return self.characterCollection.delete_one({'id': id})
    
    # def __calculateNextId(self):
    #     result = self.characterCollection.find_one({}, {'id': 1, '_id': 0},sort=[('id', -1)])
        
    #     return (result['id'] + 1) if result else 1