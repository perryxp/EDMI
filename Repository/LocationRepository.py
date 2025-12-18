from Model.Character import Character
from Model.Episode import Episode
from pymongo import ReturnDocument
from pprint import pprint

class LocationRepository:
    locationCollection = None
    episodeCollection = None
    characterCollection = None

    def __init__(self, db):
        self.locationCollection = db.getCollection("rick&morty", "locations")
        self.episodeCollection = db.getCollection("rick&morty", "episodes")
        self.characterCollection = db.getCollection("rick&morty", "characters")

    def findOne(self, id):
        location = self.locationCollection.find_one({'id': id}, {'_id': 0})
        if location:
            self._attachEpisodeReference(location)
            self._attachCharacterReference(location)
        return location

    def find(self, page, limit, filter = {}):
        skip = (page - 1) * limit
        result = self.locationCollection.find(filter, {'_id': 0}).skip(skip).limit(limit)
        locations = self._attachEpisodeReferences(list(result.sort([('id', 1)])))
        locations = self._attachCharacterReferences(locations)
        return locations
    
    def count(self, filter = {}):
        return self.locationCollection.count_documents(filter)
    
    def addLocation(self, location, id = None):
        if not id:
            id = self.__calculateNextId()
        location['id'] = id
        self.locationCollection.insert_one(location)
        return self.findOne(location['id'])
    
    def updateLocation(self, location, session = None):
        return self.locationCollection.find_one_and_update(
            {'id': location['id']},
            {'$set': location},
            session = session,
            projection={"_id": 0},
            return_document=ReturnDocument.AFTER         
        )
    
    def deleteLocation(self, id):
        return self.locationCollection.delete_one({'id': id})
    
    def __calculateNextId(self):
        result = self.locationCollection.find_one({}, {'id': 1, '_id': 0},sort = [('id', -1)])
        
        return (result['id'] + 1) if result else 1
    
    def _attachEpisodeReference(self, location):
        location['episodes'] = self.findEpisodesByLocation(location['id'])
        return location
    
    def _attachEpisodeReferences(self, locations):
        for location in locations:
            self._attachEpisodeReference(location)
        return locations
    
    def findEpisodesByLocation(self, locationId):
        episodes = list(self.episodeCollection.find({'locations.id': locationId}))
        return [Episode.getReferenceData(ep) for ep in episodes]
    
    def _attachCharacterReference(self, location):
        location['residents'] = self.findCharactersByLocation(location['id'])
        self.findCharactersByLocation(location['id'])
        return location
    
    def _attachCharacterReferences(self, locations):
        for location in locations:
            self._attachCharacterReference(location)
        return locations
    
    def findCharactersByLocation(self, locationId):
        characters = list(self.characterCollection.find({'location.id': locationId}))
        return [Character.getReferenceData(ep) for ep in characters]
