import os
import sys

DATA_FILE = "student_grades.txt"


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def format_score(value):
    return f"{value:.2f}"


def calculate_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def calculate_average_and_grade(student):
    average = (student["test1"] + student["test2"] + student["test3"]) / 3.0
    student["average"] = average
    student["grade"] = calculate_grade(average)


def load_records(filename):
    records = []
    if not os.path.exists(filename):
        return records

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                value = line.strip()
                if not value:
                    continue
                parts = value.split("|")
                if len(parts) != 7:
                    print(f"Warning: malformed line {line_number} skipped.")
                    continue
                name, student_id, t1, t2, t3, avg, grade = parts
                try:
                    student = {
                        "name": name,
                        "id": student_id,
                        "test1": float(t1),
                        "test2": float(t2),
                        "test3": float(t3),
                        "average": float(avg),
                        "grade": grade,
                    }
                    records.append(student)
                except ValueError:
                    print(f"Warning: invalid numeric data on line {line_number} skipped.")
    except IOError as error:
        print(f"Error loading records: {error}")
    return records


def save_records(filename, records):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in records:
                row = "|".join(
                    [
                        student["name"],
                        student["id"],
                        format_score(student["test1"]),
                        format_score(student["test2"]),
                        format_score(student["test3"]),
                        format_score(student["average"]),
                        student["grade"],
                    ]
                )
                file.write(row + "\n")
    except IOError as error:
        print(f"Error saving records: {error}")


def prompt_for_score(prompt_text):
    while True:
        value = input(prompt_text).strip()
        try:
            score = float(value)
            if score < 0 or score > 100:
                print("Please enter a score between 0 and 100.")
                continue
            return score
        except ValueError:
            print("Invalid value. Enter a numeric score like 88.5.")


def add_student(records):
    print("\nAdd New Student Record")
    name = input("Student name: ").strip()
    if not name:
        print("Student name cannot be blank.")
        return
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be blank.")
        return

    test1 = prompt_for_score("Test 1 score: ")
    test2 = prompt_for_score("Test 2 score: ")
    test3 = prompt_for_score("Test 3 score: ")

    student = {
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": 0.0,
        "grade": "",
    }
    calculate_average_and_grade(student)
    records.append(student)
    save_records(DATA_FILE, records)
    print(f"\nStudent record for {name} added successfully.")


def display_students(records):
    if not records:
        print("\nNo student records available.")
        return

    print("\nStudent Records")
    header = f"{'Name':<20} {'ID':<12} {'Test1':>6} {'Test2':>6} {'Test3':>6} {'Average':>8} {'Grade':>6}"
    print(header)
    print("-" * len(header))

    for student in records:
        print(
            f"{student['name']:<20} {student['id']:<12} {format_score(student['test1']):>6} "
            f"{format_score(student['test2']):>6} {format_score(student['test3']):>6} "
            f"{format_score(student['average']):>8} {student['grade']:>6}"
        )


def class_statistics(records):
    if not records:
        print("\nNo records to calculate statistics.")
        return

    averages = [student["average"] for student in records]
    highest = max(averages)
    lowest = min(averages)
    class_avg = sum(averages) / len(averages)

    print("\nClass Statistics")
    print(f"Highest average: {format_score(highest)}")
    print(f"Lowest average:  {format_score(lowest)}")
    print(f"Class average:   {format_score(class_avg)}")


def search_student(records):
    if not records:
        print("\nNo records available to search.")
        return

    search_name = input("\nEnter student name to search: ").strip().lower()
    if not search_name:
        print("Search term cannot be blank.")
        return

    matches = [student for student in records if search_name in student["name"].lower()]
    if not matches:
        print(f"No students found matching '{search_name}'.")
        return

    print(f"\nFound {len(matches)} result(s):")
    header = f"{'Name':<20} {'ID':<12} {'Test1':>6} {'Test2':>6} {'Test3':>6} {'Average':>8} {'Grade':>6}"
    print(header)
    print("-" * len(header))
    for student in matches:
        print(
            f"{student['name']:<20} {student['id']:<12} {format_score(student['test1']):>6} "
            f"{format_score(student['test2']):>6} {format_score(student['test3']):>6} "
            f"{format_score(student['average']):>8} {student['grade']:>6}"
        )


def get_menu_choice():
    print("\nStudent Grade Calculator")
    print("1 - Add new student record")
    print("2 - Show all student records")
    print("3 - Show class statistics")
    print("4 - Search student by name")
    print("ESC - Exit program")
    print("Enter a number or press ESC:")

    try:
        if os.name == "nt":
            import msvcrt
            while True:
                key = msvcrt.getch()
                if key == b"\x1b":
                    return "ESC"
                if key in b"1234":
                    print(key.decode())
                    return key.decode()
        else:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while True:
                    key = sys.stdin.read(1)
                    if key == "\x1b":
                        print()
                        return "ESC"
                    if key in "1234":
                        print(key)
                        return key
                    if key == "\r" or key == "\n":
                        continue
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception:
        choice = input("Choice: ").strip()
        if choice.lower() == "esc":
            return "ESC"
        return choice


def main():
    records = load_records(DATA_FILE)
    if records:
        print(f"Loaded {len(records)} student record(s) from {DATA_FILE}.")
    else:
        print("No saved student records found. Starting with an empty list.")

    while True:
        choice = get_menu_choice()
        if choice == "1":
            add_student(records)
        elif choice == "2":
            display_students(records)
        elif choice == "3":
            class_statistics(records)
        elif choice == "4":
            search_student(records)
        elif choice == "ESC":
            print("\nSaving records and exiting...")
            save_records(DATA_FILE, records)
            break
        else:
            print("Invalid selection. Choose 1, 2, 3, 4 or press ESC.")

    print("Goodbye!")


if __name__ == "__main__":
    main()
