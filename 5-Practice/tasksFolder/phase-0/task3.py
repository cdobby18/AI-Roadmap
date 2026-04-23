"""

Task 1. Login Authentication System - Done

    - 3 login attempts before lockout

    Output:
        Username: admin
        Password: 1234

        Login Fialed (2 Attempts Left)
        Login Successful

Task 2. File Notes System - Done

    - save notes into file and retrieve them

    Output:
        1. Add Note
        2. View Notes

        Notes:
            - Learn Python
            - Build AI Systems

"""
# Task 1
import os

correctUN = "coloma"
correctPW = "coloma123hehe@"
max_attempt = 3
attempt = 0

while attempt < max_attempt :
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == correctUN and password == correctPW:
        print("Login Successful!")
        break

    else:
        attempt = attempt + 1
        remaining_attempts = max_attempt - attempt

        if remaining_attempts > 0:
            print(f"Login Failed! {remaining_attempts}")
        else:
            print("Account Locked")
            break

# Task 2
notes_file = "notes.txt"

while True:
    print("\n1. Add Note")
    print("2. View Notes")
    print("3. Exit")

    option = input("Enter your option: ")

    # Add Note
    if option == "1":
        note = input("Enter your note: ")

        with open(notes_file, "a") as file:
            file.write(note + "\n")

        print("Note Saved")

    # View Notes
    elif option == "2":
        if os.path.exists(notes_file):
            with open(notes_file, "r") as file:
                content = file.read()

            if content.strip() == "":
                print("No notes yet.")
            else:
                print("\nNotes:")
                print(content)
        else:
            print("No notes yet.")

    # Exit
    elif option == "3":
        print("Exit Program Successfully")
        break

    else:
        print("Invalid Option")
        