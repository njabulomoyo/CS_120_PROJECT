# Healthcare System Implementation Guide

## 1. Authentication Module

### Patient Authentication (CHINYEMBA)
- Create login and signup pages for patients
- Store patient registration data in `patients.csv`
- Required fields: email, password, personal details, and insurance information
- Implement "Sessions" for patients
- Dependencies: patients.csv

### Doctor Authentication (AD)
- Implement login-only functionality for doctors
- Validate against existing credentials in `doctors.csv`
- No signup option for doctors (pre-existing accounts only)
- Implement "Sessions" for doctors
- Dependencies: doctors.csv

## 2. Dashboard

### Patient Dashboard (Robert)

#### Core Functions Required
1. `get_patient()`
   - Fetch appointment records from `appointments.csv`
   - Display both upcoming and past appointments
   - Filter by status (pending/passed)
   - Dependencies: appointments.csv

2. `get_billing()`
   - Retrieve billing information from `billing.csv`
   - Show payment status and outstanding amounts
   - Link bills to corresponding appointments via Appointment_ID
   - Dependencies: billing.csv, appointments.csv

3. `update_patient()`
   - Allow patients to edit their profile in `patients.csv`
   - Update personal information and insurance details
   - Validate data before saving
   - Dependencies: patients.csv

4. `get_prescriptions()`
   - Fetch prescription history from `prescriptions.csv`
   - Display medication details and instructions
   - Show prescription date and prescribing doctor
   - Dependencies: prescriptions.csv, patients.csv, doctors.csv

### Doctor Dashboard (Shadrack)

#### Core Functions Required
1. `view_doctor_appointments()`
   - Display appointments from `appointments.csv`
   - Filter by status (past/pending)
   - Sort by date/time
   - Dependencies: appointments.csv, doctors.csv

2. `create_prescription()`
   - Create new entries in `prescriptions.csv`
   - Auto-populate patient details from `appointments.csv` and update status
   - Check patient insurance status from `patients.csv`
   - Automatically generate billing entry in `billing.csv` with "not paid" status
   - Dependencies: prescriptions.csv, appointments.csv, patients.csv, billing.csv

### Appointment Scheduling Rules
- Available time slots: 30-minute intervals
- Hours: 9 AM to 5 PM
- Working days: Monday to Friday only
- No weekend appointments
- Booking window: Next 7 days starting from the following day (to avoid validation issues with same-day appointments)

## 3. Existing Core Functions Reference

### Authentication Functions
```python
login_required()  # Decorator for protecting routes
signup()         # Handle user registration
login()          # Process user login
logout()         # Handle user logout
```

### Dashboard Functions
1. `get_patient(email)`
   - Retrieves user information from CSV
   - Returns user data dictionary

2. `update_patient(email, details)`
   - Updates user profile information
   - Validates and saves changes

3. `get_user_appointments(email)`
   - Fetches all appointments for a user
   - Returns appointment list

4. `is_time_slot_available(doctor, date, time_slot)`
   - Checks appointment slot availability
   - Prevents double bookings

5. `get_available_dates()`
   - Returns available dates for the next 7 days
   - Excludes weekends

6. `book_appointment_helper(doctor, date, time_slot, user_email, user_name)` and `book_appointments()`
   - Handles appointment creation
   - Validates slot availability
   - Creates appointment record

## 4. Integration and Testing Sprint (AD, Chinyemba, Njabulo)

### Final Integration and Testing
- Integrate helper functions and main Python modules in app.py
- Conduct comprehensive UI testing
- Implement error handling and validation
- Perform cross-browser testing

### Future Sprint Considerations
1. Deployment
   - Evaluate migration to PythonAnywhere
   - Set up production environment
   - Configure domain settings

2. Enhanced Security
   - Implement email OTP for sign-ups
   - Add appointment confirmation emails
   - Implement session management

3. AI Integration
   - Evaluate LangChain CSV agents for data processing
   - Implement automated reporting
   - Develop smart scheduling recommendations

## 5. UI/UX Implementation (Njabulo)

### Base Template Structure
*Base HTML is used to reuse key components of the Flask web app
- Consistent header with hospital logo
- Responsive sidebar navigation
- Standard footer with copyright and navigation links
- Flash message system for user notifications

### Template-Specific Requirements

#### Authentication Pages
- **Login (`login.html`)**
  - Clean, centered form layout
  - Email and password fields with validation
  - Link to signup page

- **Signup (`signup.html`)**
  - Grid-based form layout
  - Comprehensive user details collection
  - Client-side validation using `needs-validation`
  - Mobile-responsive design

#### Dashboard Views
- **Main Dashboard (`main_dashboard.html`)**
  - Display appointments, prescriptions, and booking
  - Include booking form
  - Implement real-time slot availability updates using a calendar
  - Enforce booking window (next 7 days starting tomorrow)
  - Jinja Variables: `user`, `appointments`, `doctors`

- **Account Management (`account.html`)**
  - Profile information display
  - Collapsible edit form
  - Jinja Variables: `user['First_Name']`, `user['Last_Name']`, `user['Email']`, `user['Address']`, `user['Mobile_Number']`

#### Feature Pages
- **Appointments (`appointments.html`)**
  - Display upcoming/previous appointments
  - Implement dynamic time slot selection
  - Include Ajax-powered doctor availability check
  - Jinja Variables: `appointments`, `appointment.Doctor`, `appointment.Time`, `appointment.Booking_Time`

- **Billing (`billing.html`)**
  - Organize tables by billing types
  - Include status indicators (paid/pending)
  - Implement color-coded payment status
  - Use responsive table layout

- **Prescriptions (`prescriptions.html`)**
  - Display current and previous prescription tables
  - Include medication details with usage instructions
  - Implement clean, readable typography

### JavaScript Requirements
- Time slot update function for appointment booking
- Form validation handlers
- Bootstrap components initialization
- AJAX calls for doctor availability

### Data Display Patterns
- Use Jinja2 loops for dynamic content
- Implement conditional rendering for empty states
- Include flash message system for user feedback
- Maintain consistent date and time formatting

### Accessibility Requirements
- Include ARIA labels for interactive elements
- Use semantic HTML structure
- Ensure color contrast compliance
- Implement mobile-first responsive design

### Integration Points
- Flash message system for backend notifications
- Form submission handlers
- Dynamic content loading
- Session management for user data

## 6. Project Structure and Data Constraints

### Project Structure
```
flask_clinic_app/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Project dependencies
├── README.md              # Documentation
├── IMPLEMENTATION_GUIDE.md              # IMPLEMENTATION_GUIDE.md
├── modules/               # Function modules
│   ├── main.py           # Main functions
│   ├── helper.py         # Helper functions
│
│
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── auth/             # Authentication templates
│   │   ├── login.html
│   │   └── signup.html
│   ├── patient/          # Patient dashboard templates
│   │   ├── dashboard.html
│   │   ├── appointments.html
│   │   ├── billing.html
│   │   └── prescriptions.html
│   └── doctor/           # Doctor dashboard templates
│       ├── dashboard.html
│       └── prescriptions.html
│
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   └── img/
│
└── data/                 # CSV data files
    ├── patients.csv
    ├── doctors.csv
    ├── appointments.csv
    ├── billing.csv
    └── prescriptions.csv
```

### Data Columns and Constraints

#### billing.csv
```
Columns:
- Email (string, required)
- Date (YYYY-MM-DD format)
- Details (string)
- Cost (numeric)
- Insurance Amount (numeric)
- Paid (boolean: True/False)
- Appointment_ID (string, format: A001)
```

#### appointments.csv
```
Columns:
- Appointment_ID (string, format: A001)
- Email (string, required)
- Date (YYYY-MM-DD format)
- Time (HH:MM format)
- Doctor_ID (string, format: D001)
- Status (string: "Pending"/"Passed")
```

#### patients.csv
```
Columns:
- Name (string)
- Email (string, unique, required)
- Number (string, 10 digits)
- Address (string)
- DOB (YYYY-MM-DD format)
- Sex (string: "Male"/"Female")
- Insurance (boolean: True/False)
- Password (string)
```

#### prescriptions.csv
```
Columns:
- Email (string, required)
- Date (YYYY-MM-DD format)
- Drug (string)
- Diagnosis (string)
- Doctor_ID (string, format: D001)
```

## 7. Integration Notes
- Follow existing CSV structure using provided dummy data as reference
- Modify existing functions where applicable
- Use descriptive function names (e.g., `add_patient`, `update_prescription`)
- Create helper functions for complex operations
- Include comprehensive code comments
- Add main and helper functions in modules directory
- Write descriptive commit messages

## 8. Repository References
- Original Main Logic: https://github.com/Chinyemba-ck/CS_210
- UI Repository: https://github.com/AdrDube/CS_210/tree/dashboard
