from datetime import datetime , timedelta
import csv

def get_timeslots():
    return [ f"{hour:02d}:{minute:02d}"
            for hour in range(9, 17)
            for minute in range(0, 60, 30)
        ]

def get_available_dates():
    #gets dates available for the next 2 weeks
    dates = []
    start_date = datetime.now().date() + timedelta(days=1)
    for i in range(14):
        current_date = start_date + timedelta(days=i)
        # Exclude weekends (5 = Saturday, 6 = Sunday)
        if current_date.weekday() not in [5, 6]:
            dates.append(current_date.strftime('%Y-%m-%d'))
    return dates

def generate_appointment_id(existing_ids):
    if not existing_ids:
        return "A001"
    last_id = max(existing_ids)
    last_number = int(last_id[1:])
    return f"A{last_number + 1:03d}"

def is_time_slot_available(doctor, date, time_slot):
    #TODO
    return True
