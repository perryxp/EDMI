from Model import Character

class CharacterRepository:
    db = None
    characterCollection = None

    def __init__(self, db):
        self.db = db
        self.characterCollection = self.db.getCollection("rick&morty", "characters")

    def getCharacter(self, id):
        return self.characterCollection.find_one({'id': id}, {'_id': 0})

    def getCharacters(self):
        return list(self.characterCollection.find({}, {'_id': 0}))
    
    def addCharacter(self, character):
        id = self.__calculateNextId()
        character['id'] = id
        return self.characterCollection.insert_one(
            character.__dict__ if isinstance(character, Character) else character
        )
    
    def updateCharacter(self, id, character):
        character.pop('id', None)
        return self.characterCollection.update_one(
            {'id': id},
            {'$set': character.__dict__ if isinstance(character, Character) else character}            
        )
    
    def deleteCharacter(self, id):
        return self.characterCollection.delete_one({'id': id})
    
    def __calculateNextId(self):
        id = self.characterCollection.find({}, {'id': 1, '_id': 0}).sort('id', -1).limit(1)
        return id + 1