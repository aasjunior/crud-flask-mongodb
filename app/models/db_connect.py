from pymongo import MongoClient, errors
from models.db_config import DBConfig

class DBConnect:
    def __init__(self, collection_name):
        host, port, db_name, username, password = DBConfig.get_db_config()
        #self.client = MongoClient(f'mongodb://{username}@{host}:{port}/{db_name}?authMechanism=SCRAM-SHA-1', serverSelectionTimeoutMS = 5000)
        self.client = MongoClient(f'mongodb://localhost:27017', serverSelectionTimeoutMS = 5000)

        try:
            self.client.server_info()
        except errors.ServerSelectionTimeoutError as err:
            raise Exception("Não foi possível estabelecer conexão com o MongoDB: ", err)
        
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]