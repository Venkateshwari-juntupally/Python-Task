import csv
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from os.path import basename

import pandas as pd
import schedule
import whois


def get_whois_data(domains):
    received_data = []
    for section in domains:
        try:
            w = whois.whois(section)
            name = w.name
            email = w.email
            phone = w.phone
            date_of_registration= w.creation_date
            received_data.append([name,section, email, phone, date_of_registration])
        except Exception as e:
            log_error(f"Error extracting WHOIS data for {section}: {str(e)}")
    return received_data


def store_data_in_csv (data):
    filename = f"whois_data_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Extracted data stored in {filename}")


def send_email (data):
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    recipient_email = "recipient_email@example.com"

    subject = f"WHOIS Data -data {datetime.datetime.now().strftime('%Y-%m-%d')}"
    body = "Please find attached the WHOIS data for newly registered domains."
    attachment = f"whois_data_{datetime.datetime.now().strftime('%Y%m%d')}.csv"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = COMMASPACE.join([recipient_email])
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with open(attachment, "rb") as file:
        part = MIMEText(file.read(), "csv")
        part.add_header("Content-Disposition", f"attachment; filename={basename(attachment)}")
        message.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        log_error(f"Error sending email: {str(e)}")


def log_error(error_message):
    with open("error.log", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {error_message}\n")


def run_script():
    # List of newly registered domains
    domains = ["example1.com", "example2.com", "example3.com"]

    # Extract WHOIS data
    received_data = get_whois_data(domains)

    # Store data in CSV
    store_data_in_csv(received_data)

    # Send email with data
    send_email(received_data)
date_of_registration
# Schedule the script to run daily at a specified time
schedule.every().day.at("10:00").do(run_script)

while True:
    schedule.run_pending()
