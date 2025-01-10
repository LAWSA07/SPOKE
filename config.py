import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    
    # Your Firebase Config
    FIREBASE_CONFIG = {
        "apiKey": "AIzaSyBObVkw0CpFx3hkUOli6SDaDSCw08VSKEw",
        "authDomain": "spoke-b3cf0.firebaseapp.com",
        "projectId": "spoke-b3cf0",
        "storageBucket": "spoke-b3cf0.firebasestorage.app",
        "messagingSenderId": "1058672736321",
        "appId": "1:1058672736321:web:913ec9c949f43f3b60eec0",
        "measurementId": "G-240WGZW5BP"
    } 