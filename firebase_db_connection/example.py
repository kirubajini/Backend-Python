import firebase_admin
from firebase_admin import credentials
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from firebase_admin import db

app = Flask(__name__)# flask api

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate(
    "C:\\Users\\HOME\\PycharmProjects\\pythonProject1\\firebase_db_connection\\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://home-app-8a577-default-rtdb.firebaseio.com/'
})

# Set your SMTP email and password here
smtp_email = 'viththiarul67@gmail.com'  # Replace with your SMTP email
smtp_password = 'CWURrjTgOcF29V7h'  # Replace with your SMTP password
# Send a confirmation email using SMTP
smtp_server = 'smtp-relay.brevo.com'  # Replace with your email provider's SMTP server
smtp_port = 587  # Replace with the appropriate port (587 for TLS, 465 for SSL, etc.)


# Function to check if an input is a valid phone number
def is_valid_phone(phone):
    # You may need to adjust the validation criteria for phone numbers
    # In this example, we check if the input consists of digits and is 10 characters long.
    return phone.isdigit() and len(phone) == 10


# Function to check if an email address is a valid Gmail address
def is_valid_gmail(email):
    return email.lower().endswith("@gmail.com")


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print("data: ", data)

    # Check if required fields are present
    if "input" not in data or "password" not in data or "fullname" not in data or "confirmpassword" not in data:
        return jsonify({"error": "Missing details"}), 400

    input_value = data['input']
    password = data['password']
    fullname = data['fullname']
    confirmpassword = data['confirmpassword']

    print("input_value: ", input_value)

    # Determine if the input is an email or a phone number
    if '@' in input_value:  # Check if "@" is present, assuming it's an email
        email = input_value
        if not is_valid_gmail(email):
            return jsonify({"error": f"'{email}' is not a valid Gmail address. Email not sent."}), 400
        # Check if the email already exists in your Firebase Realtime Database
        ref = db.reference('client')
        clients = ref.get()
        if clients:
            for client_id, client_data in clients.items():
                if client_data['email'] == email:
                    return jsonify({"error": "Email already exists"}), 400
    else:  # Assuming it's a phone number
        phone = input_value
        if not is_valid_phone(phone):
            return jsonify({"error": "Invalid phone number format"}), 400

    if password != confirmpassword:
        print("Password does not match. Enter the same password")
        return jsonify({"error": "Password does not match. Enter the same password"}), 400

    # If the email or phone number does not exist, proceed with registration
    ref = db.reference('client')
    new_client_ref = ref.push()
    new_client_ref.set({
        'email': email if '@' in input_value else None,  # Store email if provided
        'phone': phone if '@' not in input_value else None,  # Store phone number if provided
        'password': password,
        'fullname': fullname,
        'confirmpassword': confirmpassword
    })

    if '@' in input_value:  # If it's an email, send an email confirmation
        # Send a confirmation email
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = email
        msg['Subject'] = 'Registration Confirmation'
        message_body = f'Hi {email} You have successfully registered your account'
        msg.attach(MIMEText(message_body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, email, msg.as_string())
    else:  # If it's a phone number, send an SMS (you'll need to implement this part)
        send_confirmation_sms(phone, fullname)

    return jsonify({"message": "User registered successfully"})


# Function to send an SMS confirmation message (you'll need to implement this)
def send_confirmation_sms(phone, fullname):
    # This is a placeholder function. You should integrate with an SMS gateway service to send actual SMS messages.
    # Replace this with the actual code to send an SMS.
    print(f"Sending confirmation SMS to {phone} for user {fullname}")


if __name__ == '__main__':
    app.run(debug=True)
