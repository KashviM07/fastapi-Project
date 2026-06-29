from database import collection

def create_user(user_data):
    return collection.insert_one(user_data)

def get_user(username):
    return collection.find_one({"username": username})

def get_user_login(username, password):
    return collection.find_one({
        "username": username,
        "password": password
    })

def update_user(username, data):
    return collection.update_one(
        {"username": username},
        {"$set": data}
    )
