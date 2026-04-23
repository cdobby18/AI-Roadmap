""" 
Task 1. Banking System CLI

    - deposit, withdraw, save balance to file.

    Output:
        Balance: 1000
        Deposit: 500
        Withdraw: 500
        New Balance: 1000

Task 2. Modular Python System

    - split program into main.py, utils.py, auth.py

    Output:
        AI System Running...
            1. Login
            2. Register
            3. Exit

"""
# Task 1

while True:
    print("Welcome to Banking System CLI \n")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Exit")

    option = input("Enter your option: ")

    if option == "1":
        depositAmount = float(input("Deposit Amount: "))
        
        try:
            with open("balance.txt", "r") as file:
                new_bal = float(file.read())
        except:
            new_bal = 0.0
        
        new_bal += depositAmount

        with open("balance.txt", "w") as file:
            file.write(str(new_bal))
            print(f"New Balance: {new_bal}")
    
    elif option == "2":
        withdrawAmount = float(input("Withdraw Amount: "))

        try:
            with open("balance.txt", "r") as file:
                new_bal = float(file.read())
        except:
            new_bal = 0.0
        
        if withdrawAmount > new_bal:
            print("Insufficient Balance!")
        else:
            new_bal -= withdrawAmount

        with open("balance.txt", "w") as file:
            file.write(str(new_bal))
            print(f"New Balance: {new_bal}")
    
    elif option == "3":
        try:
            with open("balance.txt", "r") as file:
                balance = float(file.read())
        except:
            balance = 0.0
        
        print(f"Current Balance: {balance}")
    
    elif option == "4":
        print("Exit Program Successfuly")
        break
    
    else:
        print("Invalid Option")
        
        



    