import pyodbc
import app

# Database configuration
DATABASE = 'Driver={SQL Server};Server=.\\SQLEXPRESS;Database=CardiacRiskPredictor;Trusted_Connection=yes;'


def get_db_connection():
    return pyodbc.connect(DATABASE)

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Login table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Login'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE Login (
                UserId VARCHAR(50) PRIMARY KEY,
                Password VARCHAR(50),
                EmailId VARCHAR(100)
            )
        ''')

    # Create PatientDetails table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PatientDetails'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE PatientDetails (
                PatientID VARCHAR(50) PRIMARY KEY,
                Name VARCHAR(100),
                Age INT,
                Gender VARCHAR(10),
                Height FLOAT,
                Weight FLOAT
            )
        ''')

    # Create HealthRecord table
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'HealthRecord'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE HealthRecord (
                PatientID VARCHAR(50) PRIMARY KEY,
                LDLCholesterol FLOAT,
                HDLCholesterol FLOAT,
                TotalCholesterol FLOAT,
                BP FLOAT,
                FBS FLOAT,
                MaxHR FLOAT,
                RestingECG VARCHAR(50),
                Exercise BIT,
                NoofMajorVessels INT,
                ChestPainType VARCHAR(50),
                Alcoholic BIT,
                HeartPatient BIT,
                BMI FLOAT,
                Smoking BIT
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

def insert_user_details(user_id, password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Login (UserId, Password, EmailId) VALUES (?, ?, ?)', (user_id, password, email))
    conn.commit()
    cursor.close()
    conn.close()

def insert_patient_details(patient_id, name, age, gender, height, weight):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PatientDetails (PatientID, Name, Age, Gender, Height, Weight) VALUES (?, ?, ?, ?, ?, ?)',
                   (patient_id, name, age, gender, height, weight))
    conn.commit()
    cursor.close()
    conn.close()

def insert_health_record(patient_id, ldl_chol, hdl_chol, total_chol, bp, fbs, max_hr, resting_ecg, exercise, major_vessels,
                         chest_pain_type, alcoholic, heart_patient, bmi, smoking):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO HealthRecord (PatientID, LDLCholesterol, HDLCholesterol, TotalCholesterol, BP, FBS, MaxHR, RestingECG,
                                 Exercise, NoofMajorVessels, ChestPainType, Alcoholic, HeartPatient, BMI, Smoking)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (patient_id, ldl_chol, hdl_chol, total_chol, bp, fbs, max_hr, resting_ecg, exercise, major_vessels,
          chest_pain_type, alcoholic, heart_patient, bmi, smoking))
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
    cursor.execute('UPDATE Login SET Password = ?, EmailId = ? WHERE UserId = ?', (password, email, user_id))
    conn.commit()
    cursor.close()
    conn.close()
