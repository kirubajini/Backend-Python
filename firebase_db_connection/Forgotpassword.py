import firebase_admin
from firebase_admin import credentials
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from firebase_admin import db
from flask_cors import CORS

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


# Function to check if an email address is a valid Gmail address
def is_valid_gmail(email):
    return email.lower().endswith("@gmail.com")


@app.route('/forgot', methods=['POST'])
def signup():
    # data means comes from postman
    data = request.get_json()
    print("data: ", data)

    # Check if required fields are present
    if "password" not in data or "confirmpassword" not in data:
        return jsonify({"error": "Missing details"}), 400

    password = data['password']
    confirmpassword = data['confirmpassword']

    # Check if the email already exists in your Firebase Realtime Database
    ref = db.reference('client')
    clients = ref.get()

    if clients:
        for client_id, client_data in clients.items():
            print("client_data: ", client_data)
            if password == client_data.get('password'):
                print("New password matches old password. Please use a different password.")
                return jsonify({"error": "New password matches old password. Please use a different password"}), 400

            if password != confirmpassword:
                print("Password does not match. Enter the same password")
                return jsonify({"error": "Password and confirmpassword do not match"}), 400

            # If the email exists, the new password is not equal to the old password, and the passwords match,
            # update the password in Firebase
            ref.child(client_id).update({
                'password': password,
                'confirmpassword': confirmpassword
            })
            return jsonify({"message": "Password changed successfully"})

            # Send a confirmation email
            # msg = MIMEMultipart()
            # msg['From'] = smtp_email
            # msg['To'] = email
            # msg['Subject'] = 'Password Update Successfully'
            # message_body = f'Hi {email}, You have successfully changed your password'
            # msg.attach(MIMEText(message_body, 'plain'))

            # with smtplib.SMTP(smtp_server, smtp_port) as server:
            #     server.starttls()
            #     server.login(smtp_email, smtp_password)
            #     server.sendmail(smtp_email, email, msg.as_string())

    # If the email doesn't exist, return an error
    # return jsonify({"error": "Email does not exist"}), 400


if __name__ == '__main__':
    app.run(port=9000,debug=True)
