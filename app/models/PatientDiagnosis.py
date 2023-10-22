from models.db_config import DBConnect
from bson import ObjectId

class PatientDiagnosis(DBConnect):
    def __init__(self):
        super().__init__('patient_diagnosis')

    def create(self, data, patient_id):
        medicamentos = data.get('medicamentos', [])
        medicamentos_dict = [{'nome': item.get('nome', ''), 'quantidade': item.get('quantidade', 0)} for item in medicamentos]

        data_copy = data.copy()
        data_copy.pop('medicamentos', None)
        data_copy.pop('medicamentos[][nome]', None)
        data_copy.pop('medicamentos[][quantidade]', None)
        
        data_copy['medicamentos'] = medicamentos_dict
        data_copy['patient_id'] = ObjectId(str(patient_id))

        return self.collection.insert_one(data_copy)

    
    def get_by_patient_id(self, id):
        return self.collection.find_one({
            '_id': ObjectId(id)
        })