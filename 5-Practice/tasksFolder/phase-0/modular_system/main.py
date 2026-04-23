from auth import login, register

print("AI System Running...")

while True:
    print("\n1. Login")
    print("2. Register")
    print("3. Exit")

    option = input("Enter your option: ")

    if option == "1":
        login()

    elif option == "2":
        register()

    elif option == "3":
        print("Exiting system...")
        break

    else:
        print("Invalid option")