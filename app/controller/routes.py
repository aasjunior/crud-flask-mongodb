from flask import Flask, render_template, request, redirect, url_for, session, send_file, make_response
from models.Patient import Patient
from models.PatientDiagnosis import PatientDiagnosis
from .utils.helpers import clear_tmp, ImageProcessor
from io import BytesIO

patient_model = Patient()

def init_app(app):

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/patient', methods=['GET', 'POST'])
    def patient():
        if request.method == "POST":
            image = request.files['image']
            temp_image_path = ImageProcessor.save_as_png(image)
            session['patient_data'] = request.form.to_dict()
            session['patient_image_path'] = temp_image_path
            return redirect(url_for('patient_diagnosis'))
        return render_template('patient.html')

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
                print(f'NOVO PACIENTE: {new_patient.inserted_id}')
                #patient_diagnosis_model.create(request.form, new_patient.inserted_id)
                session.clear()
                clear_tmp()
            return redirect(url_for('patients'))
        return render_template('patient_diagnosis.html')

