import csv
import json
from random import randint

def get_patient(email, user_csv, doctors_csv):
    try:
        with open(user_csv, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row["Email"] == email, email, row["Email"])
                if row['Email'] == email:
                    print(row["Password"])
                    return {
                        "Name": row["Name"],
                        "Email": row["Email"],
                        "Number": row["Number"],
                        "Address": f"{row['AddressLine1']}, {row['AddressLine2']}".strip(', '),
                        "AddressLine1": row["AddressLine1"],
                        "AddressLine2": row["AddressLine2"],
                        "DOB": row["DOB"],
                        "Sex": row["Sex"],
                        "HasInsurance": row["HasInsurance"].lower() == 'true',
                        "Insurance": row["Insurance"],
                        "Password": row["Password"],
                        "Country": row["Country"],
                        "State": row["State"],
                        "City": row["City"],
                        "ZipCode": row["ZipCode"],
                        "role":"Patient"
                    }
        with open(doctors_csv, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # print(row["Email"] == email, email, row["Email"])
                if row['Email'] == email:
                    print(row["Password"])
                    return {
                        "Name": row["Name"],
                        "Email": row["Email"],
                        # "Address": f"{row['AddressLine1']}, {row['AddressLine2']}".strip(', '),
                        "Sex": row["Sex"],
                        "Password": row["Password"],
                        "role": "Doctor",
                         "doctor_id": row["Doctor_ID"]
                    }
        return None
    except FileNotFoundError:
        print(f"Error: File not found.")
        return None
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return None



def add_patient(email, details, user_csv):
    try:
        # Define fieldnames to match the new comprehensive structure
        fieldnames = [
            "Name", "Email", "Number", "AddressLine1", "AddressLine2",
            "DOB", "Sex", "HasInsurance", "Insurance", "Password",
            "Country", "State", "City", "ZipCode"
        ]

        # Open file in append mode
        with open(user_csv, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Determine insurance status and details
            has_insurance = bool(details.get("Insurance") and details["Insurance"] != "TBD")
            insurance_provider = details.get("Insurance", {}).get("Provider", "") if has_insurance else ""

            # Write a row with all details
            patient_row = {
                "Email": email,
                "Name": details.get("Name", ""),
                "Number": details.get("Number", ""),
                "AddressLine1": details.get("AddressLine1", details.get("Address", "").split(',')[0].strip()),
                "AddressLine2": details.get("AddressLine2", details.get("Address", "").split(',')[1].strip() if ',' in details.get("Address", "") else ""),
                "DOB": details.get("DOB", "TBD"),
                "Sex": details.get("Sex", "TBD"),
                "HasInsurance": str(has_insurance).lower(),  # Convert to lowercase string for CSV
                "Insurance": insurance_provider,
                "Password": details.get("Password", ""),
                "Country": details.get("Country", ""),
                "State": details.get("State", ""),
                "City": details.get("City", ""),
                "ZipCode": details.get("ZipCode", "")
            }

            writer.writerow(patient_row)
            print(f"Patient with email {email} successfully added.")
            return True
    except FileNotFoundError:
        print(f"Error: File {user_csv} not found.")
        return False
    except Exception as e:
        print(f"Error adding patient: {e}")
        return False




def get_appointments(patient_email, appointments_csv):
    """
    Retrieve all appointments for a patient from a CSV file based on their email.

    Parameters:
        patient_email (str): The email of the patient whose appointments are needed.
        appointments_csv (str): Path to the CSV file containing appointment data.

    Returns:
        list: A 2D list where each sub-list contains
              [Appointment_ID, Date, Time, Doctor_ID, Status].
              Returns an empty list if no appointments are found.
    """
    appointments = []
    try:
        with open(appointments_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Email'] == patient_email:
                    appointments.append([
                        row["Appointment_ID"],
                        row["Date"],
                        row["Time"],
                        row["Doctor_ID"],
                        row["Status"]
                    ])
        return appointments
    except FileNotFoundError:
        print(f"Error: File {appointments_csv} not found.")
        return []
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return []


def get_billings(email, billings_csv):
    billings = []
    try:
        with open(billings_csv, mode='r') as file:
            reader = csv.DictReader(file)

            # Iterate through each row in the CSV
            for row in reader:
                if row['Email'] == email:
                    # Append billing details as a list
                    billings.append([
                        row["Date"],
                        row["Details"],
                        row["Cost"],
                        row["Insurance Amount"]
                    ])
        return billings
    except FileNotFoundError:
        print(f"Error: File {billings_csv} not found.")
        return []
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return []



def update_patient(email, details, user_csv):
    try:
        with open(user_csv, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            fieldnames = reader.fieldnames
        for row in rows:
            if row['Email'] == email:
                for key, value in details.items():
                    row[key] = value
                updated = True
                break

        with open(user_csv, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True
    except FileNotFoundError:
        print(f"Error: File {user_csv} not found.")
        return False
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def get_prescriptions(email, prescriptions_csv):
    prescriptions = []
    try:
        with open(prescriptions_csv, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row.get('Email') == email:
                    prescriptions.append({
                        "Date": row.get("Date"),
                        "Drug": row.get("Drug"),
                        "Diagnosis": row.get("Diagnosis"),
                        "Doctor_ID": row.get("Doctor_ID")
                    })

        if prescriptions:
            print(f"Found {len(prescriptions)} prescriptions for {email}.")
        else:
            print(f"No prescriptions found for {email}.")

        return prescriptions

    except FileNotFoundError:
        print(f"Error: File {prescriptions_csv} not found.")
        return []
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def get_doctors(doctors_csv):
    # only name and sex
    doctors= []
    try:
        with open(doctors_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
               doctors.append(row)
        return doctors

    except FileNotFoundError:
        print(f"Error: File {doctors_csv} not found.")
        return []
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def get_doctor(id, doctor_csv):
    try:
        with open(doctor_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Doctor_ID'] == id:
                    return {
                        "Name": row["Name"],
                        "Password": row["Password"]
                    }
        return None
    except FileNotFoundError:
        print(f"Error: File not found.")
        return None
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return None


def view_doctor_appointments(doc_id, appointments_csv):
    try:
        with open(appointments_csv, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            appointments = []
            for row in reader:
                if row['Doctor_ID'] == doc_id:
                    appointments.append(row)
            return appointments
    except FileNotFoundError:
        print(f"Error: File not found.")
        return None
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return None

def view_doctor_prescriptions(id, prescriptions_csv):
    #TODO
    return None


def get_patients(patients_csv):
    try:
        with open(patients_csv, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            patients = []
            for row in reader:
                patients.append(row)
        return patients
    except FileNotFoundError:
        print(f"Error: File not found.")
        return None
    except KeyError as e:
        print(f"Error: Missing expected column in the CSV file: {e}")
        return None

def append_to_file(file_path, text):
    try:
        with open(file_path, 'a') as file:
            file.write(text + '\n')
        print(f"Successfully appended to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
#TODO get_doctor_appointments, get_doctor prescriptions
#WARN If the input is not in title case there will be an error
#REFACTOR Use regex for checking or use a dropdown menu instead of typing on the frontend


#text format should be CSV billing format: Email, Date, Details
def add_billing(email, date, details, inventory="../data/medical_inventory.json", output_path="../data/billing.csv"):
    try:
        details = details.title()
        data = open(inventory, "r")
        inventory_data = json.load(data)

        if details not in inventory_data:
            return "Check Medication spelling"

        dosage, quantity, price_per_unit = inventory_data[details]
        insurance_amount = randint(1,50)
        text_list =list(map(str, [email, date, details, price_per_unit, insurance_amount]))
        
        text = ",".join(text_list)

        append_to_file(output_path, text)

    except Exception as e:
        return f"An error occurred: {e}"


def add_prescription(email, date, drug, diagnosis, doctor_id, prescriptions_csv='../data/prescriptions.csv'):
    try:
        drug = drug.title()
        diagnosis = diagnosis.title()

        text_list = [email, date, drug, diagnosis, doctor_id]
        text = ",".join(text_list)
        append_to_file(prescriptions_csv, text)

    except Exception as e:
        return f"An error occured: {e}"


