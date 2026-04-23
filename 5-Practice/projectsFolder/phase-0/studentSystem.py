"""
PROJECT: CLI STUDENT MANAGEMENT SYSTEM

    Goal:
        - Build a terminal-based system that behaves like a lightweight in-memory database for managing student records.

    Features:
        - Add student (name, age, grade)
        - View all students
        - Delete student by name or ID
        - Find top-performing student
        - Validate input (no empty values, age must be number)

    Output:
        === STUDENT SYSTEM ===
        1. Add Student
        2. View Students
        3. Delete Student
        4. Top Student
        5. Exit

        > Add Student
        Name: John
        Age: 21
        Grade: 90
        Student added successfully

        > View Students
        1. John - 90
        2. Anna - 95

        Top Student: Anna (95)

"""
from auth import login, register
from studentManager import add_student, view_students, delete_student, top_student


def student_menu():

    while True:

        print("\n==== STUDENT SYSTEM ====")
        print("1. Add Students")
        print("2. View Students")
        print("3. Delete Students")
        print("4. Top Student")
        print("5. Logout")

        choice = input("Enter your option: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            delete_student()

        elif choice == "4":
            top_student()

        elif choice == "5":
            break

        else:
            print("Invalid option.")


def main():

    while True:

        print("\n==== WELCOME ====")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            if login():
                student_menu()

        elif choice == "2":
            register()

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()