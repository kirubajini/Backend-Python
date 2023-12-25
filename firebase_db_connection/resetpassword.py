import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dns.resolver  # Install the dnspython library using pip
import logging
import random

# Set up logging
# logging.basicConfig(filename='email.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Email configuration
smtp_server = 'smtp-relay.brevo.com'
smtp_port = 587  # Port for TLS
smtp_username = 'viththiarul67@gmail.com'  # Your email address
smtp_password = 'CWURrjTgOcF29V7h'  # Your email password or app-specific password
from_email = 'viththiarul67@gmail.com'
to_email = 'kirusasiva99@gmail.com'  # Replace with the email you want to send to
subject = 'Your OTP'
otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
message_body = f'Your OTP is: {otp}'


# Function to check if an email address is a valid Gmail address
def is_valid_gmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email)


# Function to check if an email address is hosted on Google's servers
def is_google_mail(email):
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.query(domain, 'MX')
        for mx in mx_records:
            if 'google.com' in str(mx):
                return True
    except dns.resolver.NXDOMAIN:
        return False
    return False


# Create a logger
logger = logging.getLogger('email_sender')

try:
    if not is_valid_gmail(to_email):
        logger.error(f"'{to_email}' is not a valid Gmail address. Email not sent.")
    elif not is_google_mail(to_email):
        logger.error(f"'{to_email}' is not hosted on Google. Email not sent.")
    else:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(message_body, 'plain'))

        # Create an SMTP client session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())

        logger.info('Email sent successfully.')
except Exception as e:
    logger.error(f'Email sending failed:{str(e)}')