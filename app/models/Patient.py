from models.db_connect import DBConnect
from models.db_config import ImageProcessor
from datetime import datetime
from bson.binary import Binary
from werkzeug.utils import secure_filename
from bson import ObjectId
import tempfile
import os

class Patient(DBConnect):
    def __init__(self):
        super().__init__('patients')

    def create(self, data, image):
        png_image_path = ImageProcessor.save_as_png(image)
        with open(png_image_path, 'rb') as f:
            encoded_image = Binary(f.read())

        # Crie uma cópia mutável de 'data'
        data_copy = data.to_dict()
        data_copy['image'] = encoded_image
        data_copy['createdAt'] = datetime.now()

        return self.collection.insert_one(data_copy)    

    def get_all(self):
        return self.collection.find()

    def get_by_id(self, id):
        return self.collection.find_one({
            '_id': ObjectId(id)
        })