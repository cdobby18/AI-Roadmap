"""
Task 1. To-Do CLIP App

    - create system with add/remove/view tasks stored in a list

    Output:
        1. Add Task
        2. Remove Task
        3. View Tasks
        4. Exit

        Please select an option: 3

        View Tasks:
            - Study Python
            - Build ML Project

Task 2. Student Dictionary System

    - store student names + grades and allow to add/update/view/delete it


"""
# Task 1
print("Welcome to AI Engineering 101")

task = []

while True:
    print("\n--- MENU ---")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. View Tasks")
    print("4. Exit")

    option = input("Enter option: ")

    # Add Task
    if option == "1":
        user_task = input("Enter Task: ")
        task.append(user_task)
        print("Task added!")

    # Remove Task
    elif option == "2":
        if len(task) == 0:
            print("No tasks to remove.")
        else:
            print("\nCurrent Tasks:")
            for i, t in enumerate(task, start=1):
                print(f"{i}. {t}")

            user_task = input("Enter exact task name to remove: ")

            if user_task in task:
                task.remove(user_task)
                print("Task removed!")
            else:
                print("Task not found.")

    # View Tasks
    elif option == "3":
        if len(task) == 0:
            print("No tasks yet.")
        else:
            print("\nYour Tasks:")
            for i, t in enumerate(task, start=1):
                print(f"{i}. {t}")

    # Exit
    elif option == "4":
        print("Exiting program...")
        break

    else:
        print("Invalid option. Try again.")

# Task 2
student = {}
grade = []

while True:
    print("1. Add Student")
    print("2. Update Student Grade")
    print("3. View Students List")
    print("4. Delete Student")
    print("5. Exit")

    option = int(input("Enter your option: "))

    # Add Student:
    if option == 1:
        add_student = input("Enter name of Student: ")
        add_grade = int(input("Enter your Grade: "))

        student[add_student] = add_grade
        print("Student Added")
    
    # Update Student Grade:
    elif option == 2:
        student_name = input("Enter Student Name: ")

        if student_name in student:
            update_grade = int(input("New Grade: "))
            student[student_name] = update_grade
            print("Grade Updated")
        else:
            print("Student not found")
    
    # View List
    elif option == 3:
        if len(student) == 0:
            print("No Students")
        else:
            for student_name, grade in student.items():
                print(student_name, ": ", grade)
    
    # Delete Student
    elif option == 4:
        student_name = input("Enter Student Name to Delete: ")

        if student_name in student:
            del student[student_name]
            print("Student  Deleted")
        else:
            print("Student not found")

    else:
        print("Thank you for using our system")
        break


