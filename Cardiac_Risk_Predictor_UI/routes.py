import json
import requests
import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, render_template, request, session, url_for, jsonify, flash
from flask_login import current_user, fresh_login_required,UserMixin, login_user,login_required, logout_user
from database import insert_user_profile, update_user_profile,insert_login_details,insert_login_activity,insert_logout_activity, get_user_by_username,get_patient_details_id,get_profile_by_username, get_user_by_password, insert_patient_details, insert_prediction_result

def send_http_post_request(url, payload):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error occurred during the request: {e}')
    return None
            
def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def userprofile():
        try:             
            if request.method == 'POST':
                # Fetch data from the POST request
                name    = request.form['name']
                email   = request.form['email']
                user_id = request.form['user_id']
                address = request.form['address']
                phone   = request.form['phone']
            
                user = get_profile_by_username(user_id)
                if user:
                    update_user_profile(patient_id=user_id, user_id=user_id, name=name, email=email,address=address, phone_number=phone)                    
                else:
                    insert_user_profile(patient_id=user_id, user_id=user_id, name=name, email=email,address=address, phone_number=phone)

                # Return a response indicating the success of the update
                return render_template('patient_details.html',user=current_user)

            # Fetch and display user profile if logged in
            if(current_user):
                user_profile = get_profile_by_username(current_user.user_id)
    
            return render_template('user_profile.html',user=current_user, user_profile=user_profile)

        except Exception as e:
            return render_template('error.html', error=str(e))

    @app.route('/registration', methods=['GET', 'POST'])
    @app.route('/registration', methods=['GET', 'POST'])
    def registration():
        try: 
            if request.method == 'POST':
                # Fetch data from the POST request
                username    = request.form['username']
                password    = request.form['password']
                confirmpwd  = request.form.get('confirmPassword')
                
                # Check if the user already exists
                user = get_user_by_username(username)
                if user:
                    flash('User already registered. Please use a different username.', category='error')
                elif ' ' in username:  # Check for spaces in username
                    flash('Username cannot contain spaces.', category='error')
                elif username == '':
                    flash('Username must be filled in', category='error')
                elif password != confirmpwd:
                    flash('Passwords don\'t match.', category='error')
                elif len(password) < 7:
                    flash('Password must be at least 7 characters.', category='error')
                elif ' ' in password:  # Check for spaces in password
                    flash('Password cannot contain spaces.', category='error')
                elif not re.search('[A-Z]', password):  # Check for at least one uppercase letter
                    flash('Password must contain at least one uppercase letter.', category='error')
                elif not re.search('[!@#$%^&*(),.?":{}|<>]', password):  # Check for at least one special character
                    flash('Password must contain at least one special character.', category='error')
                else:
                    insert_login_details(username, password)#Insert user data
                    new_user = get_user_by_username(username)
                    login_user(new_user, remember=True,duration=None,force=True)
                    flash('Account created!', category='success')
                    return render_template('login.html', user=current_user)

            return render_template('registration.html', user=current_user)

        except Exception as e:
            return render_template('error.html', error=str(e))

    # Define the login route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        try:
            if request.method == 'POST':
                # Fetch data from the POST request
                username = request.form['username']
                password = request.form['password']

                # Retrieve user by username and password from the database
                user = get_user_by_password(username, password)
                
                if user:
                    if username == '':
                        flash('Username must be filled in', category='error')
                    else:
                        flash('Logged in successfully!', category='success')
                        login_user(user, remember=True,duration=None,force=True)
                        insert_login_activity(username)
                        return redirect(url_for('userprofile', user=current_user))
                else:
                    flash('Username or password is incorrect.', category='error')
                    return render_template("login.html", user=current_user)

            return render_template("login.html", user=current_user)

        except Exception as e:
            return render_template('error.html', error=str(e))

    # Define the logout route
    @app.route('/logout')
    @login_required
    def logout():
        insert_logout_activity(current_user.user_id)
        logout_user()
        return redirect(url_for('login'))

    @app.route('/patient_details', methods=['GET', 'POST'])
    @login_required
    def patient_details():
        try: 
            
            # Fetch data from the POST request
            if request.method == 'POST':
                patient_id  = current_user.user_id     
                age         = int(request.form['age'])
                sex         = int(request.form['sex'])
                cp          = int(request.form['cp'])
                trestbps    = int(request.form['trestbps'])
                restecg     = int(request.form['restecg'])
                chol        = int(request.form['chol'])
                fbs         = int(request.form['fbs'])
                thalach     = int(request.form['thalach'])
                exang       = int(request.form['exang'])
                oldpeak     = float(request.form['oldpeak'])
                slope       = int(request.form['slope'])
                ca          = int(request.form['ca'])
                thal        = int(request.form['thal'])
            

                # Call the insert_patient_data function with the fetched data
                insert_patient_details(patient_id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)

                # Call prediction api
                url = 'https://cardiac-risk-predictor-api.onrender.com/predict'  
                payload = [{
                    "age": age,
                    "sex": sex,
                    "cp":cp,
                    "trestbps": trestbps,
                    "chol" : chol,
                    "fbs" : fbs,
                    "restecg": restecg,
                    "thalach" : thalach,
                    "exang" :exang,
                    "oldpeak" : oldpeak,
                    "slope": slope,
                    "ca" :ca,
                    "thal" : thal
                }]

                response = send_http_post_request(url, payload)
                if response:
                    risk_score = None
                    suggestion = None
                    if(response['prediction_result'] == '[1]'):
                        prediction_result = "High risk of heart disease"
                        suggestion = (
                           "\nFollow Medical Advice\n" 
                          "\nPhysical Activity as advised\n" 
                          "\nEat Mindfully\n"
                        )
                        risk_score = 1
                    else:
                        prediction_result = "No risk"
                        suggestion = ( 
                            " \nStay Healthy\n"
                           "\nEat and Sleep well\n"
                          "\nPortion control\n"
                        )
                        risk_score = 0

                    patient_recid = get_patient_details_id(patient_id)
                    # Call the insert_prediction_result function with the fetched data
                    insert_prediction_result(patient_recid ,risk_score)

                    # Return a response indicating the success of the update
                    return render_template('prediction_result.html',user=current_user,  prediction_result = prediction_result, suggestion = suggestion)
                else:
                    return render_template('error.html', error="Sorry, We are experiencing an issue. Please try again later.")

            return render_template('patient_details.html', user=current_user )

        except Exception as e:
            return render_template('error.html', error=str(e))

        @app.route('/prediction_result', methods=['GET', 'POST'])
        def prediction_result():
            try: 

                return render_template('patient_details.html', user=current_user)

            except Exception as e:
                return render_template('error.html', error=str(e))
    
def go_to_profile():
        try:
            return redirect(url_for('userprofile', user=current_user))  # Redirect to the 'userprofile' route
        except Exception as e:
            return render_template('error.html', error=str(e))

