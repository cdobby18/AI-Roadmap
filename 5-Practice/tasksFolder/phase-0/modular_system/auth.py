from utils import save_user, load_users


def register():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    users = load_users()

    if username in users:
        print("User already exists")
    else:
        save_user(username, password)
        print("Registration Successful")


def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    users = load_users()

    if username in users and users[username] == password:
        print("Login Successful")
    else:
        print("Invalid Credentials")