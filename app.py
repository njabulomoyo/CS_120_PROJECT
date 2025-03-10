

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from jinja2 import FileSystemLoader

from modules import get_timeslots, get_appointments, get_billings, get_patient, update_patient, get_doctor, view_doctor_appointments, append_to_file
from modules import get_available_dates, get_patients, get_prescriptions, add_patient, get_doctors, is_time_slot_available, view_doctor_prescriptions
from functools import wraps
import csv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Define the path to the data directory
DATA_DIR = os.path.join(BASE_DIR, 'data')
PATIENTS_CSV = os.path.join(DATA_DIR, 'patients.csv')

DOCTORS_CSV = os.path.join(DATA_DIR, 'doctors.csv')
APPOINTMENTS_CSV = os.path.join(DATA_DIR, 'appointments.csv')
BILLING_CSV = os.path.join(DATA_DIR, 'billing.csv')
PRESCRIPTIONS_CSV = os.path.join(DATA_DIR, 'prescriptions.csv')

# Login required decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session:
                flash('Please login first.')
                return redirect(url_for('login'))
            if session['role'] != role:
                flash('You are not authorized to be on this page.')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('main_dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email'].strip()

        # Check if email already exists
        if get_patient(email, PATIENTS_CSV):
            flash('Email already registered')
            return redirect(url_for('signup'))


        # Prepare patient details dictionary
        details = {
            "Name": f"{request.form['first_name'].strip()} {request.form['last_name'].strip()}",
            "Number": request.form['mobile'].strip(),
            "Password": request.form['password'].strip(),
            "AddressLine1": request.form['address_line1'].strip(),
            "AddressLine2": request.form.get('address_line2', '').strip(),
            "DOB": "TBD",
            "Sex": "TBD",
            "HasInsurance": str(request.form.get('has_insurance') == 'on').lower(),
            "Insurance": request.form.get('insurance_provider', '').strip() if request.form.get('has_insurance') == 'on' else "",
            "Country": request.form.get('country', '').strip(),
            "State": request.form.get('state', '').strip(),
            "City": request.form.get('city', '').strip(),
            "ZipCode": request.form.get('zip_code', '').strip()
        }


        # Add patient to CSV
        add_patient(email, details, PATIENTS_CSV)


        logger.info(f"New user registered: {email}")
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()

        password = request.form['password'].strip()

        print(email, password)
        try:
            user = get_patient(email, PATIENTS_CSV, DOCTORS_CSV)
            print(user)
            if user and user["role"] == "Patient" and user['Password'] == password:
                session['user_email'] = email
                session['role']= 'Patient'
                session['Name']= user['Name']
                logger.info(f"Successful login for user: {email}")
                flash('Logged in successfully!')
                return redirect(url_for('main_dashboard'))

            elif user and user["role"] == "Doctor" and user["Password"] == password:
                session["user_email"] = email
                session["role"] = "Doctor"
                session["Name"] = user["Name"]
                session["doctor_id"] = user["doctor_id"]
                logger.info(f"Successful login for user: {email}")
                flash('Logged in successfully!')
                return redirect(url_for('doctor/dashboard'))

            else:
                logger.warning(f"Invalid credentials for email: {email}")
                flash('Invalid email or password')
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash('An error occurred during login. Please try again.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))




@app.route('/main_dashboard')
@role_required('Patient')
def main_dashboard():

    if session:
        appointments = get_appointments(session['user_email'], APPOINTMENTS_CSV)
        prescriptions= get_prescriptions(session['user_email'], PRESCRIPTIONS_CSV)
        doctors=get_doctors(DOCTORS_CSV)
        timeslots= get_timeslots()
        return render_template('main_dashboard.html',
                             user=session,
                             appointments=appointments,
                             prescriptions=prescriptions,
                             doctors=doctors,
                             time_slots=timeslots,
                             available_dates=get_available_dates())
    return redirect(url_for('logout'))




@app.route('/account')
@role_required('Patient')
def account():
    user= get_patient(session["user_email"], PATIENTS_CSV)
    if user:
        return render_template('account.html',
                             user=user)
    return redirect(url_for('logout'))

@app.route('/update_profile', methods=['POST'])
@role_required('Patient')
def update_profile():
    details = {
        'Name': f"{request.form['first_name'].strip()} {request.form['last_name'].strip()}",
        'Number': request.form['mobile'].strip(),
        'Address': request.form['address'].strip()
    }
    updated = update_patient(session['user_email'], details, PATIENTS_CSV)
    if updated:
        flash('Profile updated successfully!')
    else:
        flash('Failed to update profile')

    return redirect(url_for('account'))

@app.route('/billing')
@role_required('Patient')
def billing():
    if session:
        billing = get_billings(session['user_email'], BILLING_CSV)
        return render_template('billing.html',
                             user=session, billing=billing)
    return redirect(url_for('logout'))


@app.route('/prescriptions')
@role_required('Patient')
def prescriptions():
    if session:
        prescriptions=get_prescriptions(session['user_email'], PRESCRIPTIONS_CSV)
        return render_template('prescriptions.html',
                             user=session, prescriptions=prescriptions
                             )
    return redirect(url_for('logout'))



@app.route('/appointments')
@role_required('Patient')
def appointments():
    if session:
        appointments = get_appointments(session['user_email'], APPOINTMENTS_CSV)
        return render_template('appointments.html',
                             user=session,
                             appointments=appointments,)
    return redirect(url_for('logout'))



@app.route('/book_appointment', methods=['POST'])
@role_required('Patient')
def book_appointment():
    #TODO
    return redirect(url_for('main_dashboard'))

@app.route('/get_available_slots/<doctor>/<date>')
def available_slots(doctor, date):
    slots = [slot for slot in get_timeslots() if is_time_slot_available(doctor,date, slot )]
    return jsonify({'slots': slots})



@app.route('/doctor/login', methods=['GET','POST'])
def doctor_login():
    if request.method == 'POST':
        id = request.form['doctor_id'].strip()
        password = request.form['password'].strip()
        try:
            user = get_doctor(id, DOCTORS_CSV)
            if user and user['Password'] == password:
                session['doctor_id'] = id
                session['role']= 'Doctor'
                session['name']= user['Name']
                logger.info(f"Successful login for user: {id}")
                flash('Logged in successfully!')
                return redirect(url_for('doctor_dashboard'))
            else:
                logger.warning(f"Invalid credentials for email: {id}")
                flash('Invalid ID or password')
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash('An error occurred during login. Please try again.')

    return render_template('doctor_login.html')


@app.route("/create_prescription", methods=["POST"])
def create_prescription():
    print(request.form.keys())
    patient_name, patient_email, patient_phone = request.form.get('patient_details').split("##")
    dob = request.form.get('date_of_birth')
    phone = request.form.get('phone')
    medication = request.form.get('medication')
    period = request.form.get('dates')
    doctor_name, doctor_id = request.form.get('doctor_details').split("##")
    diagnosis = request.form.get("diagnosis")
    notes = request.form.get('notes')
    print(patient_email, patient_name, dob, phone, medication, period, diagnosis, doctor_name, notes)
    append_to_file(PRESCRIPTIONS_CSV,f"{patient_email},{period},{medication},{diagnosis},{doctor_id}")
    return "form submitted!"


@app.route('/doctor/dashboard')
@role_required('Doctor')
def doctor_dashboard():
    if session:
        doc_appointments = view_doctor_appointments(session['doctor_id'], APPOINTMENTS_CSV)
        doc_prescriptions= view_doctor_prescriptions(session['doctor_id'], PRESCRIPTIONS_CSV)
        patients = get_patients(PATIENTS_CSV)
        doctors = get_doctors(DOCTORS_CSV)
        print(doc_appointments)
        return render_template('doctor_dashboard.html',
                               user=session,
                               appointments=doc_appointments,
                               prescriptions=doc_prescriptions,
                               patients=patients,
                               doctors=doctors
                               )
    return redirect(url_for('logout'))

app.run(debug=True)
