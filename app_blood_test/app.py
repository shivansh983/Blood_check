from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import pandas as pd
from blood_test import HealthCheck

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

user_data = {}

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        global user_data
        user_data = {
            'name': request.form['name'],
            'gmail': request.form['gmail'],
            'contact_number': request.form['contact_number'],
            'blood_group': request.form['blood_group'],
            'gender': request.form['gender'],
            'age': int(request.form['age']) 
        }
        return redirect(url_for('upload_file'))
    return render_template('form.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'blood_report' not in request.files:
            return 'No file part'
        file = request.files['blood_report']
        if file.filename == '':
            return 'No file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the file
            data = pd.read_excel(filepath) if filepath.endswith(('xlsx', 'xls')) else pd.read_csv(filepath)
            patient = HealthCheck(
                haemoglobin=data['haemoglobin'][0],
                wbc=data['wbc'][0],
                platelets=data['platelets'][0],
                mcv=data['mcv'][0],
                pcv=data['pcv'][0],
                rbc=data['rbc'][0],
                mch=data['mch'][0],
                mchc=data['mchc'][0],
                rdw=data['rdw'][0],
                neutrophils=data['neutrophils'][0],
                lymphocytes=data['lymphocytes'][0],
                monocytes=data['monocytes'][0],
                eosinophils=data['eosinophils'][0],
                basophils=data['basophils'][0],
                gender=user_data['gender'],
                age=user_data['age'],
                name=user_data['name']
            )

            if patient.is_fit():
                result = 'Report seems all good'
            else:
                result = patient.check_blood_diseases()

            return render_template('result.html', result=result)
    return render_template('upload.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
