from flask import redirect, render_template, request, session, url_for, jsonify, flash
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from database import insert_user_profile, update_user_profile,insert_login_details, get_user_by_username,get_profile_by_username, get_user_by_password, insert_patient_details
from flask_login import current_user, fresh_login_required,UserMixin, login_user,login_required

class Login(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
            
def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    #@login_required
    def userprofile():
        try: 
            if 'username' not in session:
                return redirect(url_for('login'))

            if request.method == 'POST':
                # Fetch data from the POST request
                name = request.form['name']
                email = request.form['email']
                user_id = request.form['user_id']
                address = request.form['address']
                phone = request.form['phone']
            
                # Correct the order of arguments for insert_user_profile function
                user = get_profile_by_username(user_id)
                if user:
                    insert_user_profile(patient_id=user_id, user_id=user_id, name=name, email=email,address=address, phone_number=phone)
                else:
                    update_user_profile(patient_id=user_id, user_id=user_id, name=name, email=email,address=address, phone_number=phone)

                # Return a response indicating the success of the update
                return render_template('patient_details.html')

            return render_template('user_profile.html')

        except Exception as e:
            return render_template('error.html', error=str(e))


    @app.route('/registration', methods=['GET', 'POST'])
    def registration():
        try: 
            if request.method == 'POST':
                # Fetch data from the POST request
                username = request.form['username']
                password = request.form['password']
                confirmpwd = request.form.get('confirmPassword')
                
                # Check if the user already exists
                user = get_user_by_username(username)
                if user:
                    flash('User already registered. Please use a different username.', category='error')
                elif password != confirmpwd:
                    flash('Passwords don\'t match.', category='error')
                elif len(password) < 7:
                    flash('Password must be at least 7 characters.', category='error')
                else:
                    insert_login_details(username, password)
                    flash('Account created!', category='success')
                    return render_template('login.html')
            return render_template('registration.html')
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
                
                #user = Login.query.filter_by(username=username, password=password).first()
                user = get_user_by_password(username, password)

                if user:
                    flash('Logged in successfully!', category='success')
                    session['username'] = username
                    return redirect(url_for('userprofile'))
                else:
                    flash('Username or password is incorrect.', category='error')
                    return render_template("login.html", user=current_user)

            return render_template("login.html", user=current_user)

        except Exception as e:
            return render_template('error.html', error=str(e))

    @app.route('/patient_details', methods=['GET', 'POST'])
    #@login_required
    def patient_details():
        try: 
            if 'username' not in session:
                return redirect(url_for('login'))

            if request.method == 'POST':
            # Fetch data from the POST request
                 
                patient_id = current_user.id       
                age = int(request.form['age'])
                sex = int(request.form['sex'])
                cp = int(request.form['cp'])
                trestbps = int(request.form['trestbps'])
                restecg = int(request.form['restecg'])
                chol = int(request.form['chol'])
                fbs = int(request.form['fbs'])
                thalach = int(request.form['thalach'])
                exang = int(request.form['exang'])
                oldpeak = float(request.form['oldpeak'])
                slope = int(request.form['slope'])
                ca = int(request.form['ca'])
                thal = int(request.form['thal'])
            

                # Call the insert_patient_data function with the fetched data
                insert_patient_details(patient_id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
            
                # Return a response indicating the success of the update
                return render_template('prediction_result.html')

            return render_template('patient_details.html')

        except Exception as e:
            return render_template('error.html', error=str(e))

def health_record_exists(patient_id):
     #Function to check if the health record exists for the given patient_id
     #You can implement this function based on your database query logic
     #For simplicity, we assume it always returns False here
    return False