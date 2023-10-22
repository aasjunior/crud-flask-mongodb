from models.db_config import DBConnect
from datetime import datetime
from bson import ObjectId

class Patient(DBConnect):
    def __init__(self):
        super().__init__('patients')

    def create(self, data, image):
        # Crie uma cópia mutável de 'data'
        data_copy = data.copy()
        data_copy['image'] = image
        data_copy['createdAt'] = datetime.now()

        return self.collection.insert_one(data_copy)    

    def get_all(self):
        return self.collection.find()

    def get_by_id(self, id):
        return self.collection.find_one({
            '_id': ObjectId(id)
        })