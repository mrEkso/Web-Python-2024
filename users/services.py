from .db import users


class UserService:
    @staticmethod
    def get_all_users():
        return users

    @staticmethod
    def get_user(user_id):
        user = next((user for user in users if user.id == user_id), None)
        if not user:
            raise UserService.UserNotFound()
        return user

    @staticmethod
    def create_user(data):
        new_user = {'id': max(user.id for user in users) + 1, **data}
        users.append(new_user)
        return new_user

    @staticmethod
    def update_user(user_id, update_data):
        user = UserService.get_user(user_id)
        user.update(update_data)
        return user

    @staticmethod
    def delete_user(user_id):
        global users
        print(users)
        users = [user for user in users if user.id != user_id]

    class UserNotFound(Exception):
        pass
