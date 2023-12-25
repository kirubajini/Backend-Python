from asyncio import run

import firebase_admin
import port as port
from firebase_admin import credentials, db
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from flask_cors import CORS
import dns.resolver  # Install the dnspython library using pip


app = Flask(__name__)
CORS(app)  # Enable CORS for your app

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate(
    "C:\\Users\\HOME\\PycharmProjects\\pythonProject1\\firebase_db_connection\\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://home-app-8a577-default-rtdb.firebaseio.com/'
})

# Set your SMTP email and password here
smtp_email = 'admin@mazecode.io'  # Replace with your SMTP email
smtp_password = '8Pf0FrhGKTHzc5b4'  # Replace with your SMTP password
# Send a confirmation email using SMTP
smtp_server = 'smtp-relay.brevo.com'  # Replace with your email provider's SMTP server
smtp_port = 587  # Replace with the appropriate port (587 for TLS, 465 for SSL, etc.)
subject = 'Hello, Python Email'
message_body = 'This is a test email sent from Python.'


# Function to check if an email address is a valid Gmail address
def is_valid_gmail(email):
    return email.lower().endswith("@gmail.com")


@app.route('/sign', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print("data: ", data)

        # Check if required fields are present
        required_fields = ['email', 'password', 'fullname', 'confirmpassword']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing {field}"}), 400

        email = data['email']
        password = data['password']
        fullname = data['fullname']
        confirmpassword = data['confirmpassword']

        if not is_valid_gmail(email) or email != email.lower():
            return jsonify({"error": "Invalid Gmail address"}), 400

        # Check if the email already exists in your Firebase Realtime Database
        ref = db.reference('client')
        clients = ref.get()

        if clients:
            for client_id, client_data in clients.items():
                if client_data['email'] == email:
                    print("Email already exists")
                    return jsonify({"error": "Email already exists"}), 400

        if password != confirmpassword:
            return jsonify({"error": "Password does not match"}), 400

        # If the email does not exist and validation passes, proceed with registration
        new_client_ref = ref.push()
        new_client_ref.set({
            'email': email,
            'password': password,
            'fullname': fullname,
            'confirmpassword': confirmpassword
        })

        # Send a confirmation email
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = email
        msg['Subject'] = 'Registration Confirmation'
        message_body = f'Hi {email}, you have successfully registered your account.'
        msg.attach(MIMEText(message_body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, email, msg.as_string())

        print("User registered successfully")
        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000,debug=True)