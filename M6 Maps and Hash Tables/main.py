from schedule import Schedule


def display_menu() -> None:
    "Print the main menu options for the user."
    print("\nCourse Schedule System")
    print("1. Display full schedule")
    print("2. Search by subject")
    print("3. Search by subject and catalog number")
    print("4. Search by instructor last name")
    print("5. Quit")


def main() -> None:
    "Program entry point. Loads data from courses.csv and provides a menu-driven interface to search and display the schedule."
    schedule = Schedule()
    filename = "courses.csv"

    try:
        schedule.load_from_csv(filename)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}. "
              f"Make sure courses.csv is in the same folder as main.py.")
        return
    except Exception as ex:
        print(f"Error while loading data: {ex}")
        return

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            # Display entire schedule
            schedule.print()

        elif choice == "2":
            # Search by subject
            subject = input("Enter subject (e.g., BIO, MTH, PHY): ").strip()
            results = schedule.find_by_subject(subject)
            schedule.print(results)

        elif choice == "3":
            # Search by subject and catalog
            subject = input("Enter subject (e.g., BIO): ").strip()
            catalog = input("Enter catalog number (e.g., 141): ").strip()
            results = schedule.find_by_subject_catalog(subject, catalog)
            schedule.print(results)

        elif choice == "4":
            # Search by instructor last name
            last_name = input("Enter instructor last name: ").strip()
            results = schedule.find_by_instructor_last_name(last_name)
            schedule.print(results)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()