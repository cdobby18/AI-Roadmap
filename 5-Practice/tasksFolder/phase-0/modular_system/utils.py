"""
    UTILS.PY:
        - handles file saving and reading.

"""

USERS_FILE = "users.txt"


def save_user(username, password):
    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{password}\n")


def load_users():
    users = {}

    try:
        with open(USERS_FILE, "r") as file:
            for line in file:
                line = line.strip()  # remove \n and spaces
                if line:
                    username, password = line.split(",")
                    users[username.strip()] = password.strip()
    except FileNotFoundError:
        pass

    return users