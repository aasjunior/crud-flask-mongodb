from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify, json
from models.Patient import Patient
from models.PatientDiagnosis import PatientDiagnosis
from .utils.helpers import clear_tmp, ImageProcessor
from bson.objectid import ObjectId
from io import BytesIO
import os

patient_model = Patient()

def init_app(app):

    clear_tmp()

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/patient', methods=['GET', 'POST'])
    def patient():
        if request.method == "POST":
            image = request.files['image']
            if image.filename == '' and 'patient_image_name' not in session:
                return render_template('patient.html', error="Por favor, carregue uma imagem.")
            temp_image_path = ImageProcessor.save_as_png(image)
            session['patient_image_name'] = temp_image_path.split('\\')[-1]
            session['patient_image_path'] = temp_image_path
            session['patient_data'] = request.form.to_dict()
            return redirect(url_for('patient_diagnosis'))
        return render_template('patient.html', patient_data=session.get('patient_data', {}), patient_image_name=session.get("patient_image_name"))

    @app.route('/patients', methods=['GET'])
    def patients():
        patients = patient_model.get_all()
        return render_template('patients.html', patients=patients)

    @app.route('/image/<id>')
    def image(id):
        patient = patient_model.get_by_id(id)
        return send_file(BytesIO(patient['image']), mimetype='image/png')

   
    @app.route('/patient-diagnosis', methods=['GET', 'POST'])
    def patient_diagnosis():
        if request.method == "POST":
            patient_diagnosis_model = PatientDiagnosis()
            patient_data = session.get('patient_data')
            patient_image_path = session.get('patient_image_path')
            encoded_image = ImageProcessor.encoded_image_binary(patient_image_path)
            if patient_data and encoded_image:
                new_patient = patient_model.create(patient_data, encoded_image)
                # Obtenha os dados atuais do paciente_diagnosis da sessão
                patient_diagnosis = session.get('patient_diagnosis', {})
                # Atualize os dados atuais com os novos dados do formulário
                medicamento = request.form.get('medicamento')
                quantidade = request.form.get('quantidade')
                if medicamento and quantidade:
                    medicamentos = patient_diagnosis.get('medicamentos', [])
                    medicamentos.append({'nome': medicamento, 'quantidade': quantidade})
                    patient_diagnosis['medicamentos'] = medicamentos
                # Salve os dados atualizados na sessão
                session['patient_diagnosis'] = patient_diagnosis
                # Salve os dados no banco de dados
                patient_diagnosis_model.create(patient_diagnosis, new_patient.inserted_id)
                session.clear()
                clear_tmp()
                return redirect(url_for('patients'))

        # Recupere os dados atuais do paciente_diagnosis da sessão
        patient_diagnosis = session.get('patient_diagnosis', {})
        medicamentos = patient_diagnosis.get('medicamentos', [])
        medicamentos_quantidades = []

        if medicamentos:
            for item in medicamentos:
                medicamentos_quantidades.append({'medicamento': item.get('nome', ''), 'quantidade': item.get('quantidade', '')})

        return render_template(
            'patient_diagnosis.html', 
            patient_diagnosis=patient_diagnosis, 
            medicamentos_quantidades=medicamentos_quantidades
        )
    
    @app.route('/save-patient-diagnosis', methods=['POST'])
    def save_patient_diagnosis():
        data = request.get_json()
        session['patient_diagnosis'] = data  # Atualize os dados do paciente_diagnosis na sessão
        return jsonify(success=True)

        