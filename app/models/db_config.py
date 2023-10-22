from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

class DBConfig:
    """
    A classe DBConfig é responsável por carregar as variáveis de ambiente do arquivo .env e fornecer
    os detalhes do banco de dados quando necessário. Isso é feito para evitar a duplicação de código
    e manter a configuração do banco de dados em um único lugar.

    Métodos
    -------
    get_db_details():
        Retorna os detalhes do banco de dados como host, port, db_name, username e password.
    """
    load_dotenv()

    @staticmethod
    def get_db_config():
        host = os.getenv('MONGODB_HOST')
        port = int(os.getenv('MONGODB_PORT'))
        db_name = os.getenv('MONGODB_DATABASE')
        username = os.getenv('MONGODB_USERNAME')
        password = os.getenv('MONGODB_PASSWORD')

        return host, port, db_name, username, password

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
