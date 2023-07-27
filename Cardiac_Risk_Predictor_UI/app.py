from flask import Flask
from flask import redirect, render_template, request, session, url_for, jsonify
import routes
from database import create_tables, insert_user_details, insert_patient_details, insert_health_record


app = Flask(__name__)
app.secret_key = "cardiac_predictor_9876"

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# SQL configuration
#app.config['DATABASE'] = 'Driver={SQL Server};Server=DESKTOP-H7F3DUK\SQLEXPRESS;Database=CardiacRiskPredictor;Trusted_Connection=yes;'


if __name__ == '__main__':
    create_tables()  # Create tables if they don't exist
    routes.configure_routes(app)
    #app.run(debug=True)
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)