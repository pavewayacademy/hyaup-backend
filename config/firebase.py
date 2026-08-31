import firebase_admin
from firebase_admin import credentials
from config.config import settings

# Initialize Firebase Admin SDK
def init_firebase():
    """Initialize Firebase Admin SDK with service account credentials."""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin SDK initialized successfully")
        else:
            print("ℹ️ Firebase app already initialized")
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        raise