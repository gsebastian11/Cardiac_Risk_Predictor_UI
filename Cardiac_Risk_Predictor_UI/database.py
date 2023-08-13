import os
import pyodbc
import psycopg2
import datetime
import uuid
from werkzeug.security import check_password_hash

#Database configuration
#DATABASE = 'Driver={SQL Server};Server=.\\SQLEXPRESS;Database=CardiacRiskPredictor;Trusted_Connection=yes;'
#DATABASE = 'Driver={SQL Server};Server=LAPTOP-TOMKVT9U;Database=CardiacRiskPredictor;User=gifty;Password=ssgg1@3ggss;'


##local
#db_host = "dpg-cjbbu5fdb61s73f8pdk0-a.oregon-postgres.render.com"
#db_user = "admin"
#db_password = "GzYgZi2hd32JM797Oxr6imkGalLx3edV"
#db_name = "cardiacriskpredictor"

#prod
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

DATABASE = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port=5432 sslmode='require'"
def get_db_connection():
    return psycopg2.connect(DATABASE)

class Login:
    def __init__(self, user_id, username, password):
        self.id         = user_id
        self.username   = username
        self.password   = password
    def get_id(self):
        return str(self.id) 

class UserProfile:
    def __init__(self, user_id, name, email_id, address, phone_number):
        self.user_id        = user_id
        self.name           = name
        self.email_id       = email_id
        self.address        = address
        self.phone_number   = phone_number

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)

class PatientDetails:
    def __init__(self, patient_recid,patient_id):
        self.patient_recid        = patient_recid
        self.patient_id           = patient_id

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)
        
def create_tables():
    conn    = get_db_connection()
    cursor  = conn.cursor()

    # Create Login table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'login'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE Login (
                UserId VARCHAR(50) PRIMARY KEY,
                Password VARCHAR(50),
                CreatedDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ModifiedDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')   

    # Create LoginActivity table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'loginactivity'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE LoginActivity (
                ActivityId SERIAL PRIMARY KEY,
                UserId VARCHAR(50) REFERENCES Login(UserId),
                LoginTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                LogoutTime TIMESTAMP,
                CONSTRAINT CHK_LogoutTime CHECK (LogoutTime >= LoginTime)
            )
        ''')

    # Create UserProfile table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'userprofile'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE UserProfile (
                PatientID VARCHAR(50) PRIMARY KEY,                
                UserId VARCHAR(50) REFERENCES Login(UserId) ON DELETE CASCADE,
                Name VARCHAR(50),
                EmailId VARCHAR(50),
                Address VARCHAR(100),
                PhoneNumber BIGINT,
                CreatedDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ModifiedDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    # Create PatientDetails table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'patientdetails'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE PatientDetails (
                PatientRecid VARCHAR(50) PRIMARY KEY,
                PatientID VARCHAR(50) REFERENCES UserProfile(PatientID) ON DELETE CASCADE,
                name VARCHAR(50),
                age INT,
                sex FLOAT,
                cp FLOAT,
                trestbps Float,
                chol Float,
                fbs Float,
                restecg Float,
                thalach Float,
                exang Float,
                oldpeak Float,
                slope Float,
                ca Float,
                thal Float,
                CreatedDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    # Create PredictionResult table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'predictionresult'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE PredictionResult (
                PatientRecid VARCHAR(50) REFERENCES PatientDetails(PatientRecid)  ON DELETE CASCADE,
                RiskScore INT,
                CreatedDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    conn.commit()
    cursor.close()
    conn.close()      

#Insert into table Login
def insert_login_details(user_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get the current timestamp

    cursor.execute('''
        INSERT INTO Login (UserId, Password)
        VALUES (%s, %s)
    ''', (user_id, password))
    cursor.execute('''
        INSERT INTO UserProfile (
            PatientID, UserId, Name, EmailId, Address, PhoneNumber
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (user_id, user_id, '', '', '', 123456789))
    conn.commit()
    cursor.close()
    conn.close()

def insert_login_activity(user_id):
    conn    = get_db_connection()
    cursor  = conn.cursor()


    cursor.execute('''
        INSERT INTO LoginActivity (UserId, LogoutTime)
        VALUES (%s, %s)
    ''', (user_id, None))

    conn.commit()
    cursor.close()
    conn.close()

def insert_logout_activity(user_id):
    conn    = get_db_connection()
    cursor  = conn.cursor()

    cursor.execute('''
        UPDATE LoginActivity
        SET LogoutTime = CURRENT_TIMESTAMP
        WHERE UserId = %s AND LogoutTime IS NULL
    ''', (user_id,))

    conn.commit()
    cursor.close()
    conn.close()

def insert_patient_details(patient_id, age, sex, cp, trestbps, chol, fbs, 
                           restecg, thalach, exang, oldpeak, slope, ca, thal):
    conn    = get_db_connection()
    cursor  = conn.cursor()

    current_datetime    = datetime.datetime.now()# Get the current timestamp
    patient_recid       = str(uuid.uuid4())# Generate a unique identifier using UUID    


    cursor.execute('''
        INSERT INTO PatientDetails (
            PatientRecid, PatientID, age, sex, cp, trestbps, chol, fbs, restecg, thalach,
            exang, oldpeak, slope, ca, thal, CreatedDateTime
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        patient_recid, patient_id, age, sex, cp, trestbps, chol, fbs, restecg, thalach,
        exang, oldpeak, slope, ca, thal, current_datetime
    ))

    conn.commit()
    cursor.close()
    conn.close()

def insert_user_profile(patient_id, user_id, name, email, address, phone_number):
    conn    = get_db_connection()
    cursor  = conn.cursor()

    # Get the current timestamp
    current_datetime = datetime.datetime.now()

    cursor.execute('''
        INSERT INTO UserProfile (
            PatientID, UserId, Name, EmailId, Address, PhoneNumber, CreatedDateTime, ModifiedDateTime
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (patient_id, user_id, name, email, address, phone_number, current_datetime, ''))
    
    conn.commit()
    cursor.close()
    conn.close()


def insert_prediction_result(patient_recid, risk_score):
    conn    = get_db_connection()
    cursor  = conn.cursor()

    # Get the current timestamp
    current_datetime = datetime.datetime.now()

    cursor.execute('''
        INSERT INTO PredictionResult (
            PatientRecid, RiskScore, CreatedDateTime
        )
        VALUES (%s, %s, %s)
    ''', (patient_recid, risk_score, current_datetime))
    
    conn.commit()
    cursor.close()
    conn.close()



# updates

def update_user_info(user_id, password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get the current timestamp
    current_datetime = datetime.datetime.now()
    cursor.execute('UPDATE Login SET Password = %s WHERE UserId = %s', (password, user_id))
    conn.commit()
    cursor.close()
    conn.close()

import datetime

def update_user_profile(patient_id, user_id, name, email, address, phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the current timestamp
    current_datetime = datetime.datetime.now()

    cursor.execute('''
        UPDATE UserProfile
        SET Name = %s, EmailId = %s, Address = %s, PhoneNumber = %s, ModifiedDateTime = %s
        WHERE PatientID = %s AND UserId = %s
    ''', (name, email, address, phone_number, current_datetime, patient_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()


#Select records
def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT UserId, Password FROM Login WHERE UserId = %s', (username,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        user_id, password = user_data
        user = Login(user_id, username, password)  # Create a Login instance directly
        return user
    
    return None  # User not found

def get_user_by_password(username, entered_password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT UserId, Password FROM Login WHERE UserId = %s', (username,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        user_id, hashed_password = user_data
        #if check_password_hash(hashed_password, entered_password):
        if (hashed_password == entered_password):
            user = Login(user_id, username, hashed_password)  # Create a Login instance
            return user
    return None  # User not found or incorrect password

#Select records
def get_profile_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT UserId, Name, EmailId, Address, PhoneNumber FROM UserProfile WHERE UserId = %s', (username,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        user_id = user_data[0]  # Extract the user_id from the tuple
        name = user_data[1], 
        email_id = user_data[2],
        address = user_data[3],
        phone_number = user_data[4]
        user = UserProfile(user_id,name,email_id,address,phone_number)  # Create a UserProfile instance directly
        #user = UserProfile(user_id,patient_id,name,email_id,address,phone_number)
        return user
    
    return None  # User not found

# Select records
def get_patient_details_id(patientid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT PatientRecid, PatientID FROM PatientDetails WHERE PatientID = %s', (patientid,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        patient_recid, patient_id = user_data
        return patient_recid
    
    return None  # User not found or patient details not found



