from Model.Character import Character
from pymongo import ReturnDocument

class CharacterRepository:
    characterCollection = None

    def __init__(self, db):
        self.characterCollection = db.getCollection("rick&morty", "characters")

    def findOne(self, id):
        return self.characterCollection.find_one({'id': id}, {'_id': 0})

    def find(self, page, limit, filter = {}):
        skip = (page - 1) * limit
        result = self.characterCollection.find(filter, {'_id': 0}).skip(skip).limit(limit)
        return list(result.sort([('id', 1)]))

    def count(self, filter = {}):
        return self.characterCollection.count_documents(filter)

    def addCharacter(self, character):
        id = self.__calculateNextId()
        character.id = id
        self.characterCollection.insert_one(
            character.__dict__ if isinstance(character, Character) else character
        )
        return self.findOne(character.id)
    
    def updateCharacter(self, id, character):
        if isinstance(character, Character):
            character.id = id
        else:
            character['id'] = id
        return self.characterCollection.find_one_and_update(
            {'id': id},
            {'$set': character.__dict__ if isinstance(character, Character) else character},
            projection={"_id": 0},
            return_document=ReturnDocument.AFTER         
        )
    
    def deleteCharacter(self, id):
        return self.characterCollection.delete_one({'id': id})
    
    def __calculateNextId(self):
        result = self.characterCollection.find_one({}, {'id': 1, '_id': 0},sort=[('id', -1)])
        
        return (result['id'] + 1) if result else 1