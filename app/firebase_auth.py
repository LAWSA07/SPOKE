import firebase_admin
from firebase_admin import credentials, auth
from flask import current_app

def initialize_firebase():
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred) 