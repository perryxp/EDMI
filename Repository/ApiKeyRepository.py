from datetime import datetime, timezone, timedelta

class ApiKeyRepository:
    apikeyCollection = None
    _APIKEY_REQUEST_LIMIT = 20

    def __init__(self, db):
        self.apikeyCollection = db.getCollection('rick&morty', 'apikeys')

    def findOne(self, apikey):
        return self.apikeyCollection.find_one({
            'apikey': apikey,
            '$or': [
                {'expiration': {'$gte': datetime.now(timezone.utc)}}, 
                {'expiration': {'$exists': False}}
            ]
        })

    def addTemporaryApikey(self, apikey, ttl):
        now = datetime.now(timezone.utc)
        expiration = now + timedelta(seconds=ttl)
        return self.apikeyCollection.insert_one({
            'apikey': apikey,
            'type': 'user-password-auth',
            'ttl': ttl,
            'expiration': expiration,
            'limit': self._APIKEY_REQUEST_LIMIT,
            'crated_at': now
        })