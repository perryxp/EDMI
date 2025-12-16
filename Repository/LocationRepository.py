from Model.Location import Location
from pymongo import ReturnDocument

class LocationRepository:
    locationCollection = None

    def __init__(self, db):
        self.locationCollection = db.getCollection("rick&morty", "locations")

    def findOne(self, id):
        return self.locationCollection.find_one({'id': id}, {'_id': 0})

    def find(self, page, limit, filter = {}):
        skip = (page - 1) * limit
        result = self.locationCollection.find(filter, {'_id': 0}).skip(skip).limit(limit)
        return list(result.sort([('id', 1)]))
    
    def count(self, filter = {}):
        return self.locationCollection.count_documents(filter)
    
    def addLocation(self, location):
        id = self.__calculateNextId()
        location.id = id
        self.locationCollection.insert_one(
            location.__dict__ if isinstance(location, Location) else location
        )
        return self.findOne(location.id)
    
    def updateLocation(self, id, location, session = None):

        if isinstance(location, Location):
            location.id = id
        else:
            location['id'] = id
        return self.locationCollection.find_one_and_update(
            {'id': id},
            {'$set': location.__dict__ if isinstance(location, Location) else location},
            session = session,
            projection={"_id": 0},
            return_document=ReturnDocument.AFTER         
        )
    
    def deleteLocation(self, id):
        return self.locationCollection.delete_one({'id': id})
    
    def __calculateNextId(self):
        result = self.locationCollection.find_one({}, {'id': 1, '_id': 0},sort=[('id', -1)])
        
        return (result['id'] + 1) if result else 1