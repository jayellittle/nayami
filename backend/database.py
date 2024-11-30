import firebase_admin
from firebase_admin import credentials, db
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')

try:
    cred = credentials.Certificate(BASE_DIR / './serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
    })
    posts_ref = db.reference('posts')
except Exception as e:
    print(f"Firebase initialization error: {e}")
    raise
