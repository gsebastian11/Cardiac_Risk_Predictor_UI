from flask import redirect, render_template, request, session, url_for, jsonify
from app import app
from database import insert_health_record

#Routes
#@app.route('/', methods=['GET', 'POST'])
#def home():
#     return render_template('profilePage.html')


def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        try: 
            if request.method == 'POST':
                # Fetch data from the POST request
                patient_id = request.form['patient_id']
                ldl_chol = request.form['ldl_chol']
                hdl_chol = request.form['hdl_chol']
                total_chol = request.form['total_chol']
                bp = request.form['bp']
                fbs = request.form['fbs']
                max_hr = request.form['max_hr']
                resting_ecg = request.form['resting_ecg']
                exercise = request.form['exercise']
                major_vessels = request.form['major_vessels']
                chest_pain_type = request.form['chest_pain_type']
                alcoholic = request.form['alcoholic']
                heart_patient = request.form['heart_patient']
                bmi = request.form['bmi']
                smoking = request.form['smoking']

                #if health_record_exists(patient_id):
                #    update_health_record(patient_id, ldl_chol, hdl_chol, total_chol, bp, fbs, max_hr, resting_ecg, exercise,
                #                         major_vessels, chest_pain_type, alcoholic, heart_patient, bmi, smoking)
                #else:
                insert_health_record(patient_id, ldl_chol, hdl_chol, total_chol, bp, fbs, max_hr, resting_ecg, exercise,
                                         major_vessels, chest_pain_type, alcoholic, heart_patient, bmi, smoking)

                # Return a response indicating the success of the update
                return jsonify({'message': 'Health record updated successfully'})
            return render_template('profilePage.html')
        except Exception as e:
            return render_template('error.html', error=str(e))

def health_record_exists(patient_id):
     #Function to check if the health record exists for the given patient_id
     #You can implement this function based on your database query logic
     #For simplicity, we assume it always returns False here
    return False