# Alexis Moore
# CIS261
# WK10 Student Grade Calculator

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "student_grades.txt")


def load_records(filename):
    records = []
    if not os.path.exists(filename):
        return records

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    continue
                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    record = {
                        "name": name,
                        "id": student_id,
                        "test1": float(test1),
                        "test2": float(test2),
                        "test3": float(test3),
                        "average": float(average),
                        "grade": grade,
                    }
                    records.append(record)
                except ValueError:
                    continue
    except IOError as error:
        print(f"Error loading records from {filename}: {error}")
    return records


def save_records(filename, records):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for record in records:
                file.write(
                    "|".join(
                        [
                            record["name"],
                            record["id"],
                            f"{record['test1']:.2f}",
                            f"{record['test2']:.2f}",
                            f"{record['test3']:.2f}",
                            f"{record['average']:.2f}",
                            record["grade"],
                        ]
                    )
                    + "\n"
                )
        print(f"Student records saved to {filename}.")
    except IOError as error:
        print(f"Error saving records to {filename}: {error}")


def calculate_average(test1, test2, test3):
    return (test1 + test2 + test3) / 3


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


def prompt_float(prompt_message):
    while True:
        value = input(prompt_message).strip()
        if value.upper() == "ESC":
            return None
        try:
            score = float(value)
            if score < 0 or score > 100:
                print("Please enter a score between 0 and 100.")
                continue
            return score
        except ValueError:
            print("Invalid entry. Enter a numeric value or ESC to cancel.")


def add_student(records):
    print("\nAdd New Student Record (type ESC at any prompt to cancel)")
    name = input("Student name: ").strip()
    if name.upper() == "ESC":
        print("Add student canceled.")
        return

    student_id = input("Student ID: ").strip()
    if student_id.upper() == "ESC":
        print("Add student canceled.")
        return

    test1 = prompt_float("Test 1 score: ")
    if test1 is None:
        print("Add student canceled.")
        return
    test2 = prompt_float("Test 2 score: ")
    if test2 is None:
        print("Add student canceled.")
        return
    test3 = prompt_float("Test 3 score: ")
    if test3 is None:
        print("Add student canceled.")
        return

    average = calculate_average(test1, test2, test3)
    grade = calculate_grade(average)

    record = {
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    }
    records.append(record)
    print(f"Student '{name}' added successfully with average {average:.2f} and grade {grade}.")


def display_records(records):
    if not records:
        print("\nNo student records available.")
        return

    print("\nAll Student Records")
    print("=" * 87)
    print(
        f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} {'Average':>8} {'Grade':>7}"
    )
    print("-" * 87)
    for record in records:
        print(
            f"{record['name']:<20} {record['id']:<12} "
            f"{record['test1']:7.2f} {record['test2']:7.2f} {record['test3']:7.2f} "
            f"{record['average']:8.2f} {record['grade']:>7}"
        )
    print("=" * 87)


def class_statistics(records):
    if not records:
        print("\nNo records to calculate statistics.")
        return

    averages = [record["average"] for record in records]
    highest = max(averages)
    lowest = min(averages)
    class_avg = sum(averages) / len(averages)

    print("\nClass Statistics")
    print("=" * 28)
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_avg:.2f}")
    print("=" * 28)


def search_student(records):
    if not records:
        print("\nNo student records available to search.")
        return

    query = input("Enter student name to search: ").strip()
    if query.upper() == "ESC":
        print("Search canceled.")
        return

    results = [
        record
        for record in records
        if query.lower() in record["name"].lower()
    ]

    if not results:
        print(f"No students found with name containing '{query}'.")
        return

    print(f"\nSearch results for '{query}':")
    print("=" * 87)
    print(
        f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} {'Average':>8} {'Grade':>7}"
    )
    print("-" * 87)
    for record in results:
        print(
            f"{record['name']:<20} {record['id']:<12} "
            f"{record['test1']:7.2f} {record['test2']:7.2f} {record['test3']:7.2f} "
            f"{record['average']:8.2f} {record['grade']:>7}"
        )
    print("=" * 87)


def display_menu():
    print("\nStudent Grade Calculator")
    print("1. Add new student record")
    print("2. Display all students")
    print("3. Display class statistics")
    print("4. Search student by name")
    print("5. Save records")
    print("ESC. Exit")


def main():
    records = load_records(DATA_FILE)
    if records:
        print(f"Loaded {len(records)} student record(s) from {DATA_FILE}.")
    else:
        print("No saved student records found. Starting with an empty list.")

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()
        if choice.upper() == "ESC":
            save_records(DATA_FILE, records)
            print("Exiting program. Goodbye!")
            break
        if choice == "1":
            add_student(records)
        elif choice == "2":
            display_records(records)
        elif choice == "3":
            class_statistics(records)
        elif choice == "4":
            search_student(records)
        elif choice == "5":
            save_records(DATA_FILE, records)
        else:
            print("Invalid option. Please choose 1-5 or ESC to exit.")


if __name__ == "__main__":
    main()
