from flask import redirect, render_template, request, session, url_for, jsonify
from app import app
from database import insert_user_profile, insert_login_details
from flask_login import current_user, login_required

def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    #@login_required
    def userprofile():
        try: 
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
                    username        = request.form['username']
                    password        = request.form['password']
                    confirmpwd      = request.form.get('confirmPassword')
                
                    user = Login.query.filter_by(username=username).first()
                    if user:
                        flash('User already registred.Please use different user name', category='error')                    
                    elif password != confirmpwd:
                        flash('Passwords don\'t match.', category='error')
                    elif len(password) < 7:
                        flash('Password must be at least 7 characters.', category='error')
                    else:
                        insert_login_details(username, password)
                        # Return a response indicating the success of the update
                        flash('Account created!', category='success')
                        return render_template('login.html')
            except Exception as e:
                return render_template('error.html', error=str(e))

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            try: 
                if request.method == 'POST':
                    # Fetch data from the POST request
                    username        = request.form['username']
                    password        = request.form['password']
                    user = Login.query.filter_by(username=username).first()
                    if user:
                        if check_password_hash(Login.Password, password):
                            flash('Logged in successfully!', category='success')
                            login_user(user, remember=True)
                            return redirect(url_for('userprofile.home'))
                        else:
                            flash('Incorrect password, try again.', category='error')
                    else:
                        flash('Email does not exist.', category='error')

                    return render_template("login.html", user=current_user)
                return render_template("login.html", user=current_user)
            except Exception as e:
                return render_template('error.html', error=str(e))

def health_record_exists(patient_id):
     #Function to check if the health record exists for the given patient_id
     #You can implement this function based on your database query logic
     #For simplicity, we assume it always returns False here
    return False