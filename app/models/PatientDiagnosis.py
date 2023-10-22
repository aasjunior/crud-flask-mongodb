from models.db_config import DBConnect
from bson import ObjectId

class PatientDiagnosis(DBConnect):
    def __init__(self):
        super().__init__('patient_diagnosis')

    def create(self, data, patient_id):
        medicamentos = data.getlist('medicamentos[]')
        quantidades = data.getlist('quantidade[]')

        # Transforma as listas de medicamentos e quantidades em uma lista de dicionários
        medicamentos_dict = [{'nome': m, 'quantidade': int(q)} for m, q in zip(medicamentos, quantidades)]

        data_copy = data.copy()
        # Remove os campos indesejados
        data_copy.pop('medicamentos[]', None)
        data_copy.pop('quantidade[]', None)
        
        data_copy['medicamentos'] = medicamentos_dict
        data_copy['patient_id'] = str(patient_id)
        
        return self.collection.insert_one(data_copy)
    
    def get_by_patient_id(self, id):
        return self.collection.find_one({
            '_id': ObjectId(id)
        })