import pyodbc
import app

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
                Age INT,
                Gender FLOAT,
                ChestPainType FLOAT,
                RestingBP Float,
                Cholesterol Float,
                FastingBS Float,
                RestingEcg Float,
                Thalach Float,
                ExAng Float,
                DepressionInExersise Float,
                SlopPeakExe Float,
                NumMajVessels Float,
                Thalassemia Float
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
                Gender VARCHAR(10),
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

def insert_patient_details(patient_id, age, gender, chest_pain_type, resting_bp, serum_cholestrole, fasting_bs, 
                           resting_ecg, maximum_hr, exersise_ia, dep_indu_exersise, slope_peak_exer, num_vessles, thalassemia):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PatientDetails (PatientID , UserId ,Age ,Gender ,ChestPainType ,RestingBP ,Cholesterol , FastingBS ,RestingEcg ,Thalach ,ExAng ,DepressionInExersise ,SlopPeakExe ,NumMajVessels ,Thalassemia ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (patient_id, age, gender, chest_pain_type, resting_bp, serum_cholestrole, fasting_bs, 
                    resting_ecg, maximum_hr, exersise_ia, dep_indu_exersise, slope_peak_exer, num_vessles, thalassemia))
    conn.commit()
    cursor.close()
    conn.close()

def insert_user_profile(patient_id, user_id, name, email, gender, address, phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO UserProfile (PatientID, Name, EmailId, Gender, Address, PhoneNumber)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (patient_id, name, email, gender, address, phone_number))
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


