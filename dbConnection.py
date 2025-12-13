from pymongo import MongoClient
from contextlib import contextmanager
import os

class dbConnection:
    client = None
    session = None
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

    def getCollection(self, database, collection):
        return self.client[database][collection]
    
    @contextmanager
    def transaction(self):
        with self.client.start_session() as session:
            with session.start_transaction():
                yield session