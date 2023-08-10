from flask import redirect, render_template, request, session, url_for, jsonify, flash
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from database import insert_user_profile, insert_login_details, get_user_by_username
from flask_login import current_user, fresh_login_required,UserMixin, login_user,login_required

class Login(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def userprofile():
        try: 
            #if 'username' not in session:
                #return redirect(url_for('login'))

            if request.method == 'POST':
                # Fetch data from the POST request
                name = request.form['name']
                email = request.form['email']
                user_id = request.form['user_id']
                gender = request.form['gender']
                address = request.form['address']
                phone = request.form['phone']
            
                # Correct the order of arguments for insert_user_profile function
                insert_user_profile(patient_id=user_id, user_id=user_id, name=name, email=email, gender=gender, address=address, phone_number=phone)

                # Return a response indicating the success of the update
                return jsonify({'message': 'Health record updated successfully'})

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

                # Retrieve user by username from the database
                user = get_user_by_username(username)
            
                if user:
                    if check_password_hash(user.password, password):
                        flash('Logged in successfully!', category='success')
                        login_user(user, remember=True)
                        return redirect(url_for('userprofile'))
                    else:
                        flash('Incorrect password, try again.', category='error')
                else:
                    flash('Username does not exist.', category='error')
                    return render_template("login.html", user=current_user)

            return render_template("login.html", user=current_user)

        except Exception as e:
            return render_template('error.html', error=str(e))

def health_record_exists(patient_id):
     #Function to check if the health record exists for the given patient_id
     #You can implement this function based on your database query logic
     #For simplicity, we assume it always returns False here
    return False