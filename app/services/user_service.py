from app.db.database import db


def get_users(skip: int = 0, limit: int = 10):
    users = list(db.users.find().skip(skip).limit(limit))
    return users


def get_user(user_id: int):
    user = db.users.find_one({"_id": user_id})
    return user


def get_user_by_username(username: str):
    user = db.users.find_one({"username": username})
    return user


def create_user(user_data):
    result = db.users.insert_one({
        "username": user_data.username,
        "hashed_password": user_data.password,
        "is_admin": user_data.is_admin
    })
    user = db.users.find_one({"_id": result.inserted_id})
    return user


def update_user(user_id: int, user_data):
    result = db.users.update_one(
        {"_id": user_id},
        {"$set": {
            "username": user_data.username,
            "hashed_password": user_data.password,
            "is_admin": user_data.is_admin
        }},
        return_document=True
    )
    updated_user = db.users.find_one({"_id": user_id})
    return updated_user


def delete_user(user_id: int):
    user = db.users.find_one_and_delete({"_id": user_id})
    return user
