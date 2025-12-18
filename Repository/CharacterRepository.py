from Model.Character import Character
from Model.Episode import Episode
from pymongo import ReturnDocument

class CharacterRepository:
    characterCollection = None
    episodeCollection = None

    def __init__(self, db):
        self.characterCollection = db.getCollection('rick&morty', 'characters')
        self.episodeCollection = db.getCollection('rick&morty', 'episodes')

    def findOne(self, id):
        character = self.characterCollection.find_one({'id': id}, {'_id': 0})
        if character:
            self._attachEpisodeReference(character)
        return character


    def find(self, page, limit, filter = {}):
        skip = (page - 1) * limit
        result = self.characterCollection.find(filter, {'_id': 0}).skip(skip).limit(limit)
        return self._attachEpisodeReferences(list(result.sort([('id', 1)])))

    def count(self, filter = {}):
        return self.characterCollection.count_documents(filter)

    def addCharacter(self, character, id = None, session = None):
        if not id:
            id = self.__calculateNextId()
        character['id'] = id
        self.characterCollection.insert_one(character)
        return self.findOne(id)
    
    def updateCharacter(self, character, session = None):
        return self.characterCollection.find_one_and_update(
            {'id': character['id']},
            {'$set': character},
            session = session,
            projection={"_id": 0},
            return_document=ReturnDocument.AFTER         
        )
    
    def deleteCharacter(self, id, session = None):
        return self.characterCollection.delete_one({'id': id}, session = session)
    
    def __calculateNextId(self):
        result = self.characterCollection.find_one({}, {'id': 1, '_id': 0},sort=[('id', -1)])        
        return (result['id'] + 1) if result else 1
    
    def _attachEpisodeReference(self, character):        
        episodes = self.episodeCollection.find({"characters.id": character['id']})
        character['episodes'] = [Episode.getReferenceData(ep) for ep in episodes]
        return character
    
    def _attachEpisodeReferences(self, characters):
        for character in characters:
            self._attachEpisodeReference(character)
        return characters

        