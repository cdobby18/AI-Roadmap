import json
import os

USER_FILE = "users.json"

print("test hello world")
def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def register():
    users = load_users()

    username = input("Enter new username: ")

    if username in users:
        print("Username already exists.")
        return False

    password = input("Enter password: ")

    users[username] = password
    save_users(users)

    print("Registration successful.")
    return True


def login():
    users = load_users()

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == password:
        print("Login successful.")
        return True
    else:
        print("Invalid credentials.")
        return False