students = []


def add_student():
    name = input("Enter student name: ")
    grade = float(input("Enter grade: "))

    student = {
        "name": name,
        "grade": grade
    }

    students.append(student)

    print("Student added successfully.")


def view_students():
    if not students:
        print("No students found.")
        return

    print("\nStudent List:")

    for i, student in enumerate(students):
        print(f"{i+1}. {student['name']} - {student['grade']}")


def delete_student():
    view_students()

    if not students:
        return

    index = int(input("Enter student number to delete: ")) - 1

    if 0 <= index < len(students):
        removed = students.pop(index)
        print(f"{removed['name']} deleted.")
    else:
        print("Invalid number.")


def top_student():
    if not students:
        print("No students available.")
        return

    top = max(students, key=lambda x: x["grade"])

    print("\nTop Student:")
    print(top["name"], "-", top["grade"])