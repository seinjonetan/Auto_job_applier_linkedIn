import os
import csv
from time import sleep
from random import randint
from datetime import datetime, timedelta
from setup.config import file_name, failed_file_name, logs_folder_path

# Function to search for Chrome Profiles
def find_default_profile_directory():
    # List of default profile directory locations to search
    default_locations = [
        r"%LOCALAPPDATA%\Google\Chrome\User Data",
        r"%USERPROFILE%\AppData\Local\Google\Chrome\User Data",
        r"%USERPROFILE%\Local Settings\Application Data\Google\Chrome\User Data"
    ]
    for location in default_locations:
        profile_dir = os.path.expandvars(location)
        if os.path.exists(profile_dir):
            return profile_dir
    return None


# Wait Function
def buffer(speed=0):
    if speed<=0:
        return
    elif speed <= 1 and speed < 2:
        return sleep(randint(6,10)*0.1)
    elif speed <= 2 and speed < 3:
        return sleep(randint(10,18)*0.1)
    else:
        return sleep(randint(18,round(speed)*10)*0.1)
    

# Date posted calculator
def calculate_date_posted(time_string):
    time_string = time_string.strip()
    # print_lg(f"Trying to calculate date job was posted from '{time_string}'")
    now = datetime.now()
    if "second" in time_string:
        seconds = int(time_string.split()[0])
        date_posted = now - timedelta(seconds=seconds)
    elif "minute" in time_string:
        minutes = int(time_string.split()[0])
        date_posted = now - timedelta(minutes=minutes)
    elif "hour" in time_string:
        hours = int(time_string.split()[0])
        date_posted = now - timedelta(hours=hours)
    elif "day" in time_string:
        days = int(time_string.split()[0])
        date_posted = now - timedelta(days=days)
    elif "week" in time_string:
        weeks = int(time_string.split()[0])
        date_posted = now - timedelta(weeks=weeks)
    elif "month" in time_string:
        months = int(time_string.split()[0])
        date_posted = now - timedelta(days=months * 30)
    elif "year" in time_string:
        years = int(time_string.split()[0])
        date_posted = now - timedelta(days=years * 365)
    else:
        date_posted = None
    return date_posted
    

# Failed job list update
def failed_job(job_id, job_link, resume, date_listed, error, exception, application_link, screenshot_name):
    with open(failed_file_name, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['Job ID', 'Job Link', 'Resume Tried', 'Date listed', 'Date Tried', 'Predicted reason', 'Stack Trace', 'External Job link', 'Screenshot']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0: writer.writeheader()
        writer.writerow({'Job ID':job_id, 'Job Link':job_link, 'Resume Tried':resume, 'Date listed':date_listed, 'Date Tried':datetime.now(), 'Predicted reason':error, 'Stack Trace':exception, 'External Job link':application_link, 'Screenshot':screenshot_name})
        file.close()


# Get list of applied job's Job IDs function
def get_applied_job_ids():
    job_ids = set()
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                job_ids.add(row[0])
    except FileNotFoundError:
        print_lg(f"The CSV file '{file_name}' does not exist.")
    return job_ids


def manual_login_retry(is_logged_in):
    count = 0
    while not is_logged_in():
        print_lg("Seems like you're not logged in!")
        message = "Press Enter to continue after you logged in..."
        if count > 1:
            message = "If you're seeing this message even after you logged in, type 'skip' and press Enter to continue or just press Enter to try again..."
        count += 1
        try:
            value = input(message).lower().strip()
            if value == 'skip': return
        except:
            print_lg("  --> Only type 'skip' to skip. Try again!")


def critical_error_log(possible_reason, stack_trace):
    print_lg(possible_reason, stack_trace, datetime.now())
    pass

def print_lg(*msgs):
    try:
        message = "\n".join(str(msg) for msg in msgs)
        with open(logs_folder_path+"log.txt", 'a', encoding="utf-8") as file:
            file.write(message + '\n')
        print(message)
    except Exception as e:
        critical_error_log("Log.txt is open or is occupied by another program!", e)
