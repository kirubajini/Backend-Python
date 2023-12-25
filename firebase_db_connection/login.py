import firebase_admin
from firebase_admin import credentials
from flask import Flask, request, jsonify
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


@app.route('/login', methods=['POST'])
def login():
    # Data comes from the client (e.g., Ionic app)
    data = request.get_json()

    # Check if required fields are present
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data['email']
    password = data['password']

    ref = db.reference('client')
    clients = ref.get()

    if clients:
        for client_id, client_data in clients.items():
            if client_data.get('email') == email and client_data.get('password') == password:
                # Successful login
                print("Login successfully")
                return jsonify({"message": "Login successfully"})
            else:
                print("Login Failed")
                return jsonify({"message": "Login Failed"})

    print("Incorrect email or password")
    return jsonify({"error": "Incorrect email or password"}), 401


if __name__ == '__main__':
    app.run(debug=True)