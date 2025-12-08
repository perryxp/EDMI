from dotenv import load_dotenv
from dbConnection import dbConnection

def init_extensions(app):
    load_dotenv()
    db = dbConnection()
    return db
