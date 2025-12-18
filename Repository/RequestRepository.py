from datetime import datetime, timezone

class RequestRepository:
    requestCollection = None

    def __init__(self, db):
        self.requestCollection = db.getCollection('rick&morty', 'requests')
    
    def countRequestsByApikeyAndIp(self, apikey, timestampFrom):
        return self.requestCollection.count_documents({
            'apikey': apikey, 
            'timestamp': {'$gte': timestampFrom}
        })

    def register(self, apikey, endpoint, ip):
        return self.requestCollection.insert_one({
            'apikey': apikey,
            'endpoint': endpoint,
            'ip': ip,
            'timestamp': datetime.now(timezone.utc)
        })