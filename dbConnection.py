from pymongo import MongoClient
import os

class dbConnection:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

    def getCollection(self, database, collection):
        return self.client[database][collection]
