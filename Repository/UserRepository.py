class UserRepository:
    userCollection = None

    def __init__(self, db):
        self.userCollection = db.getCollection('rick&morty', 'users')

    def findUser(self, user, password):
        return self.userCollection.find_one({'user': user, 'pass': password, 'active': True})