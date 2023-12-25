from twilio.rest import Client
from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, db
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your app

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate(
    "C:\\Users\\HOME\\PycharmProjects\\pythonProject1\\firebase_db_connection\\serviceAccountKey.json")
initialize_app(cred, {
    'databaseURL': 'https://home-app-8a577-default-rtdb.firebaseio.com/'
})

# Your Twilio API credentials
twilio_account_sid = 'ACa0660d6f16807d0a9da31412412eb452'
twilio_auth_token = 'bc44248a3d55b667e6d32a1745481c0e'
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Set your SMTP email credentials
smtp_email = 'viththiarul67@gmail.com'
smtp_password = 'CWURrjTgOcF29V7h'
smtp_server = 'smtp-relay.brevo.com'
smtp_port = 587
from_email = 'viththiarul67@gmail.com'
subject = 'Your OTP'


@app.route('/send_otp', methods=['POST'])
def send_otp():
    try:
        # Get the user input (phone or email) and the corresponding value
        data = request.get_json()
        user_input = data.get('user_input')
        value = data.get('value')

        # Generate a random OTP
        otp = str(random.randint(1000, 9999))

        if user_input == 'email':
            # Send OTP to email using SMTP
            email_msg = MIMEMultipart()
            email_msg['From'] = smtp_email
            email_msg['To'] = value
            email_body = f'Your OTP is: {otp}'
            email_msg.attach(MIMEText(email_body, 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_email, smtp_password)
                server.sendmail(smtp_email, value, email_msg.as_string())

            print(f'OTP sent to email {value} successfully.')

        # elif user_input == 'phone':
        #     # Send OTP to phone using Twilio
        #     twilio_from_number = '+13344630741'
        #     twilio_message = twilio_client.messages.create(
        #         body=f"Your OTP is {otp}",
        #         from_=twilio_from_number,
        #         to=value
        #     )
        #     print(f"SMS sent to phone {value} with SID: {twilio_message.sid}")

        return jsonify({"message": "OTP sent successfully."})

    except Exception as e:
        print(f"Error sending OTP: {str(e)}")
        return jsonify({"error": f"Error sending OTP: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(port=9001,debug=True)