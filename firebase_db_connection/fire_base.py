import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase with your project's credentials
cred = credentials.Certificate('C:\\Users\\HOME\\PycharmProjects\\pythonProject1\\firebase_db_connection\\serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://home-app-8a577-default-rtdb.firebaseio.com/'
})

# Reference to the root of your Firebase Realtime Database
root = db.reference()

# Add data to the 'users' node
users_ref = root.child('users')
new_user_ref = users_ref.push()
new_user_ref.set({
    "name": "John",
    "age": 30,

    "name": "kushi",
    "age": 24
})

# Read data from the 'users' node
users = users_ref.get()

if users:
    for user_id, user_data in users.items():
        print(f"User ID: {user_id}")
        for key, value in user_data.items():
            print(f"{key}: {value}")
else:
    print("No data found in the 'users' node.")

# Clean up resources
firebase_admin.delete_app(firebase_admin.get_app())
