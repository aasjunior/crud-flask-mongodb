from flask import Flask, render_template, request, redirect, url_for, session, send_file, make_response
from models.Patient import Patient
from models.PatientDiagnosis import PatientDiagnosis

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
            new_patient = patient_model.create(request.form, image)
            return redirect(url_for('patient_diagnosis', id=new_patient.inserted_id))
        return render_template('patient.html')

    @app.route('/patients', methods=['GET'])
    def patients():
        patients = patient_model.get_all()
        return render_template('patients.html', patients=patients)

    @app.route('/image/<id>')
    def image(id):
        patient = patient_model.get_by_id(id)
        return send_file(BytesIO(patient['image']), mimetype='image/png')

   
    @app.route('/patient-diagnosis/<id>', methods=['GET', 'POST'])
    def patient_diagnosis(id):
        if request.method == "POST":
            patient_diagnosis_model = PatientDiagnosis()
            patient_diagnosis_model.create(request.form, id)
            return redirect(url_for('patients'))
        return render_template('patient_diagnosis.html')

