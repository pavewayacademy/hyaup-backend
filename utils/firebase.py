# pyrefly: ignore [missing-import]
from firebase_admin import auth
from models.user import FirebaseUser, CreateFirebaseUser, UpdateFirebaseUser

# Helper functions to interact with Firebase

# Get user by uid
def get_user_by_uid(uid: str) -> dict:
    try:
        user = auth.get_user(uid)
        print(f"Successfully fetched user: {user}")
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise Exception(e)

# Get user by email
def get_user_by_email(email: str) -> dict:
    try:
        user = auth.get_user_by_email(email)
        print(f"Successfully fetched user: {user}")
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise Exception(e)

# Get user by phone number
def get_user_by_phone_number(phone_number: str) -> dict:
    try:
        user = auth.get_user_by_phone_number(phone_number)
        print(f"Successfully fetched user: {user}")
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise Exception(e)

# Create firebase user with email and password
def create_firebase_user(user: CreateFirebaseUser) -> dict:
    try:
        new_user = auth.create_user(
            email=user.email,
            phone_number=user.phone_number,
            password=user.password,
            display_name=user.display_name,
            photo_url=user.photo_url
        )
        print(f"Sucessfully created new user: {new_user}")
        return new_user
    except Exception as e:
        print(f"Error creating new user: {e}")
        raise Exception(e)

#Update Firebase User
def update_firebase_user(user: UpdateFirebaseUser, uid: str ) -> dict:
    try:
        updated_user = auth.update_user(uid, **user.dict())
        print(f"Successfully updated user: {updated_user}")
        return updated_user
    except Exception as e:
        print(f"Error updating user: {e}")
        raise Exception(e)

# Delete Firebase User
def delete_firebase_user(uid: str) -> dict:
    try:
        auth.delete_user(uid)
        print(f"Successfully deleted user: {uid}")
        return {"message": "User deleted successfully"}
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise Exception(e)