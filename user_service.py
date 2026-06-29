from user_repository import (
    create_user,
    get_user,
    get_user_login,
    update_user
)

def register_user_service(user):
    create_user(user.dict())

def login_service(username, password):
    return get_user_login(username, password)

def profile_service(username):
    return get_user(username)

def update_profile_service(username, data):
    return update_user(username, data)
