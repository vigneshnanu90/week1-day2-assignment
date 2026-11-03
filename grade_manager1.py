"""
Student Grade Manager (Pro Terminal Edition)
Pure Python Standard Library — No external packages required.
"""

from dataclasses import dataclass
import csv
import json
import statistics


# ANSI escape sequences for clean terminal formatting
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"


@dataclass
class Student:
    name: str
    mark: float

    @property
    def grade(self) -> str:
        if self.mark >= 90:
            return "A"
        elif self.mark >= 80:
            return "B"
        elif self.mark >= 70:
            return "C"
        elif self.mark >= 60:
            return "D"
        return "E"

    @property
    def color(self) -> str:
        """Visual color coding based on academic standing."""
        if self.grade in ("A", "B"):
            return Style.GREEN
        if self.grade == "C":
            return Style.CYAN
        if self.grade == "D":
            return Style.YELLOW
        return Style.RED


students: list[Student] = []


def get_grade(mark: float) -> str:
    """Helper satisfying the base assignment function interface."""
    return Student("", mark).grade


def prompt_valid_name() -> str:
    while True:
        name = input(f"{Style.CYAN}Enter student name: {Style.RESET}").strip()
        if name:
            return name
        print(f"{Style.RED}Error: Name cannot be blank.{Style.RESET}")


def prompt_valid_mark() -> float:
    while True:
        raw_val = input(f"{Style.CYAN}Enter mark (0 - 100): {Style.RESET}").strip()
        try:
            val = float(raw_val)
            if 0.0 <= val <= 100.0:
                return round(val, 2)
            print(f"{Style.RED}Error: Mark must be within 0 to 100.{Style.RESET}")
        except ValueError:
            print(f"{Style.RED}Error: Numeric entry required (e.g. 85 or 92.5).{Style.RESET}")


def add_student():
    name = prompt_valid_name()
    mark = prompt_valid_mark()
    students.append(Student(name=name, mark=mark))
    print(f"{Style.GREEN}✓ Successfully recorded {name} ({mark}){Style.RESET}\n")


def display_grade_histogram(marks: list[float]):
    """Renders a pure-ASCII horizontal bar chart."""
    counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    for m in marks:
        counts[get_grade(m)] += 1

    print(f"\n{Style.BOLD}Grade Distribution:{Style.RESET}")
    for grade, count in counts.items():
        bar = "█" * (count * 2)
        print(f"  {grade} [{count:>2}]: {bar}")


def show_results():
    if not students:
        print(f"{Style.YELLOW}No student records available to display.{Style.RESET}\n")
        return

    marks = [s.mark for s in students]
    highest = max(marks)
    lowest = min(marks)
    avg = sum(marks) / len(marks)
    median = statistics.median(marks)

    print("\n" + "=" * 42)
    print(f"{Style.BOLD}{'Name':<18} {'Mark':<8} {'Grade':<6} {'Badge'}{Style.RESET}")
    print("-" * 42)

    for s in students:
        badge = "★ Top" if s.mark == highest and len(students) > 1 else ""
        formatted_mark = int(s.mark) if s.mark.is_integer() else f"{s.mark:.1f}"
        print(
            f"{s.name:<18} "
            f"{formatted_mark:<8} "
            f"{s.color}{s.grade:<6}{Style.RESET} "
            f"{Style.BOLD}{badge}{Style.RESET}"
        )

    print("-" * 42)
    print(f"Average: {avg:.1f}   Median: {median:.1f}")
    print(f"Highest: {highest}   Lowest: {lowest}")
    print("=" * 42)

    # Show terminal chart
    display_grade_histogram(marks)
    print()


def export_data():
    """Allows exporting collected grades to CSV or JSON."""
    if not students:
        print(f"{Style.YELLOW}Nothing to export.{Style.RESET}\n")
        return

    print("\n1. Export to CSV (Excel compatible)")
    print("2. Export to JSON")
    fmt = input("Choose format (1-2): ").strip()

    if fmt == "1":
        filename = "grades_export.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Mark", "Grade"])
            for s in students:
                writer.writerow([s.name, s.mark, s.grade])
        print(f"{Style.GREEN}✓ Exported to {filename}{Style.RESET}\n")

    elif fmt == "2":
        filename = "grades_export.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [{"name": s.name, "mark": s.mark, "grade": s.grade} for s in students],
                f,
                indent=2,
            )
        print(f"{Style.GREEN}✓ Exported to {filename}{Style.RESET}\n")
    else:
        print(f"{Style.RED}Invalid export option.{Style.RESET}\n")


def main():
    while True:
        print(f"{Style.BOLD}--- Student Grade Manager Pro ---{Style.RESET}")
        print("1. Add Student")
        print("2. Show Results & Analytics")
        print("3. Export Grade Sheet (CSV/JSON)")
        print("4. Quit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            show_results()
        elif choice == "3":
            export_data()
        elif choice == "4":
            print(f"{Style.CYAN}Exiting application. Goodbye!{Style.RESET}")
            break
        else:
            print(f"{Style.RED}Invalid option. Enter 1 to 4.{Style.RESET}\n")


if __name__ == "__main__":
    main()