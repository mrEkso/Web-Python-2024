from bson import ObjectId
from passlib.context import CryptContext

from app.db.database import db

# CryptContext instance for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of users from the database.

    Args:
      skip (int): The number of records to skip in the database query.
      limit (int): The maximum number of records to return.

    Returns:
      list: A list of user records.
  """
    users = list(db.users.find().skip(skip).limit(limit))
    return users


def get_user(user_id: ObjectId):
    """
    Retrieve a user from the database by their ID.

    Args:
        user_id (ObjectId): The ID of the user to retrieve.

    Returns:
        dict: The user record, or None if no user was found.
    """
    user = db.users.find_one({"_id": user_id})
    return user


def get_user_by_username(username: str):
    """
    Retrieve a user from the database by their username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        dict: The user record, or None if no user was found.
    """
    user = db.users.find_one({"username": username})
    return user


def create_user(user_data):
    """
    Create a new user in the database.

    Args:
        user_data (dict): The data for the new user.

    Returns:
        dict: The newly created user record.
    """
    result = db.users.insert_one({
        "username": user_data.username,
        "hashed_password": pwd_context.hash(user_data.password),  # hash the password
        "is_admin": user_data.is_admin
    })
    user = db.users.find_one({"_id": result.inserted_id})
    return user


def update_user(user_id: ObjectId, user_data):
    """
    Create a new user in the database.

    Args:
        user_data (dict): The data for the new user.

    Returns:
        dict: The newly created user record.
        :param user_id:
    """

    update_data = {
        "username": user_data.username,
        "is_admin": user_data.is_admin
    }
    if user_data.password:
        update_data["hashed_password"] = pwd_context.hash(user_data.password)
    result = db.users.update_one(
        {"_id": user_id},
        {"$set": update_data}
    )
    updated_user = db.users.find_one({"_id": user_id})
    return updated_user


def delete_user(user_id: ObjectId):
    """
    Delete a user from the database.

    Args:
        user_id (ObjectId): The ID of the user to delete.

    Returns:
        dict: The deleted user record.
    """
    user = db.users.find_one_and_delete({"_id": user_id})
    return user


def verify_password(plain_password, hashed_password):
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
