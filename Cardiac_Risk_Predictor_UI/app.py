import routes
from flask import Flask
from database import Login
from flask import redirect, render_template, request, session, url_for, jsonify
from flask_login import UserMixin, login_user, current_user, login_required, logout_user,LoginManager
from database import create_tables, insert_login_details, insert_patient_details, get_profile_by_username,insert_user_profile, insert_prediction_result


app             = Flask(__name__)
app.secret_key  = "cardiac_predictor_9876"

login_manager               = LoginManager()
login_manager.login_view    = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_profile_by_username(user_id)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

if __name__ == '__main__':
    create_tables()  # Create tables if they don't exist
    routes.configure_routes(app)
    
    app.run()
    #import os
    #HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(os.environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    #app.run(HOST, PORT) 