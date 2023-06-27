import whois
import pandas as pd
import schedule
import time
import smtplib
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

def extract_whois_details():
    domains = ['google.com', 'amazon.com', 'facebook.com']
    
    data = pd.DataFrame(columns=['Date', 'Time', 'Domain', 'Name', 'Email', 'Phone'])

    for domain in domains:
        try:
            w = whois.whois(domain)

            # Extract the required details
            name = w.name
            email = w.email
            phone = w.phone

            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            # Add the details to the DataFrame
            data = data.append({'Date': now.split()[0],
                                'Time': now.split()[1],
                                'Domain': domain,
                                'Name': name,
                                'Email': email,
                                'Phone': phone}, ignore_index=True)
        except Exception as e:
            logging.error(f'Error extracting WHOIS details for {domain}: {str(e)}')

    # Perform deduplication and filtering if needed
    data.drop_duplicates(inplace=True)  # Remove duplicate entries
    data = data[data['Name'].notna()]  # Filter out entries without a name

    # Save the extracted details to a database or CSV file
    data.to_csv('whois_details.csv', index=False)

    # Send an email with the extracted details
    send_email(data)

# Function to send an email with the extracted details
def send_email(data):
    sender_email = 'u7569543@gmail.com'
    receiver_email = 'jvenkateshwari.99@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'u7569543@gmail.com'
    smtp_password = 'User@123'

    # Compose the email message
    subject = 'WHOIS Details for Newly Registered Domains'
    body = data.to_string(index=False)
    message = f'Subject: {subject}\n\n{body}'

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
    except Exception as e:
        logging.error(f'Error sending email: {str(e)}')

# Schedule the script to run daily at a specified time (e.g., 9:00 AM)
schedule.every().day.at('09:00').do(extract_whois_details)

# Run the scheduled tasks indefinitely
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        logging.error(f'Error during script execution: {str(e)}')
