import pyodbc
import app
from werkzeug.security import check_password_hash

# Database configuration
#DATABASE = 'Driver={SQL Server};Server=.\\SQLEXPRESS;Database=CardiacRiskPredictor;Trusted_Connection=yes;'
DATABASE = 'Driver={SQL Server};Server=LAPTOP-TOMKVT9U;Database=CardiacRiskPredictor;User=gifty;Password=ssgg1@3ggss;'


def get_db_connection():
    return pyodbc.connect(DATABASE)

class Login:
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password
    def get_id(self):
        return str(self.id) 

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)
        


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Login table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Login'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE Login (
                UserId VARCHAR(50) PRIMARY KEY,
                Password VARCHAR(50)
            )
        ''')

    # Create PatientDetails table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PatientDetails'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE PatientDetails (
                PatientID VARCHAR(50) PRIMARY KEY,
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
            )
        ''')

    # Create UserProfile table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UserProfile'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE UserProfile (
                PatientID VARCHAR(50) PRIMARY KEY,                
                UserId VARCHAR(50) REFERENCES Login(UserId),
                Name VARCHAR(50),
                EmailId VARCHAR(50),
                Address VARCHAR(100),
                PhoneNumber BIGINT
            )
        ''')

    # Create PredictionResult table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PredictionResult'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE PredictionResult (
                PatientID VARCHAR(50) PRIMARY KEY,
                RiskScore FLOAT
            )
        ''')

    conn.commit()
    cursor.close()
    conn.close()

def insert_login_details(user_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Login (UserId, Password) VALUES (?, ?)', (user_id, password))
    conn.commit()
    cursor.close()
    conn.close()

def insert_patient_details(patient_id, age, sex, cp, trestbps, chol, fbs, 
                           restecg, thalach, exang, oldpeak, slope, ca, thal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PatientDetails (PatientID , age ,sex, cp, trestbps, chol, fbs ,restecg, thalach, exang, oldpeak, slope, ca, thal ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (patient_id, age, sex, cp, trestbps, chol, fbs, 
                           restecg, thalach, exang, oldpeak, slope, ca, thal))
    conn.commit()
    cursor.close()
    conn.close()

def insert_user_profile(patient_id, user_id, name, email, address, phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO UserProfile (PatientID, UserId, Name, EmailId, Address, PhoneNumber)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (patient_id, user_id, name, email, address, phone_number))
    conn.commit()
    cursor.close()
    conn.close()

def insert_prediction_result(patient_id, risk_score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PredictionResult (PatientID, RiskScore) VALUES (?, ?)', (patient_id, risk_score))
    conn.commit()
    cursor.close()
    conn.close()


# updates

def update_user_info(user_id, password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Login SET Password = ? WHERE UserId = ?', (password, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_user_profile(patient_id, user_id, name, email, address, phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE UserProfile
        SET Name = ?, EmailId = ?, Address = ?, PhoneNumber = ?
        WHERE PatientID = ? AND UserId = ?
    ''', (name, email, address, phone_number, patient_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()


#Select records
def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT UserId, Password FROM Login WHERE UserId = ?', (username,))
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

    cursor.execute('SELECT UserId, Password FROM Login WHERE UserId = ?', (username,))
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

    cursor.execute('SELECT UserId FROM UserProfile WHERE UserId = ?', (username,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        user_id = user_data[0]  # Extract the user_id from the tuple
        #patient_id = user_data[1]
        #name = user_data[2], 
        #email_id = user_data[3],
        #address = user_data[4],
        #phone_number = user_data[5]
        user = UserProfile(user_id)  # Create a UserProfile instance directly
        #user = UserProfile(user_id,patient_id,name,email_id,address,phone_number)
        return user
    
    return None  # User not found



