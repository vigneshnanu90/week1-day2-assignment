"""
Student Grade Manager - Enhanced Edition
Pure Standard Library | Clean Terminal UI | Robust Validation
"""

from dataclasses import dataclass
import sys


class Style:
    """Terminal styling using standard ANSI escape codes."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"


@dataclass
class Student:
    name: str
    mark: float

    @property
    def grade(self) -> str:
        """Determines grade according to boundary rules[cite: 1]."""
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
    def grade_color(self) -> str:
        """Color indicator based on performance level."""
        colors = {
            "A": Style.GREEN,
            "B": Style.CYAN,
            "C": Style.BLUE,
            "D": Style.YELLOW,
            "E": Style.RED,
        }
        return colors.get(self.grade, Style.RESET)

    @property
    def formatted_mark(self) -> str:
        """Trims decimal point when mark is an exact whole integer."""
        return f"{int(self.mark)}" if self.mark.is_integer() else f"{self.mark:.1f}"


students: list[Student] = []


def is_duplicate_name(candidate_name: str) -> bool:
    """Case-insensitive check for existing names."""
    normalized = candidate_name.strip().lower()
    return any(s.name.lower() == normalized for s in students)


def prompt_student_name() -> str:
    """Collects and verifies a clean, unique name or allows cancellation."""
    while True:
        raw = input(f"{Style.CYAN}Enter student name (or type 'cancel'): {Style.RESET}").strip()

        if not raw:
            print(f"{Style.RED}Error: Name cannot be blank.{Style.RESET}")
            continue

        if raw.lower() == "cancel":
            return ""

        # Validate that the name contains sensible characters
        clean_name = " ".join(raw.split()).title()

        if is_duplicate_name(clean_name):
            print(f"{Style.RED}Error: Student '{clean_name}' already exists. Names must be unique.{Style.RESET}")
            continue

        return clean_name


def prompt_student_mark() -> float | None:
    """Collects and validates grade marks within the [0, 100] range."""
    while True:
        raw = input(f"{Style.CYAN}Enter mark (0 - 100) or 'cancel': {Style.RESET}").strip()

        if raw.lower() == "cancel":
            return None

        try:
            val = float(raw)
            if 0.0 <= val <= 100.0:
                return round(val, 2)
            print(f"{Style.RED}Error: '{val}' is outside valid boundaries. Mark must be between 0 and 100.{Style.RESET}")
        except ValueError:
            print(f"{Style.RED}Error: '{raw}' is not a valid number. Digits only.{Style.RESET}")


def add_student_entry():
    """Add student workflow with cancellation support."""
    print(f"\n{Style.BOLD}--- Register New Student ---{Style.RESET}")
    
    name = prompt_student_name()
    if not name:
        print(f"{Style.DIM}Action cancelled. Returning to main menu.{Style.RESET}\n")
        return

    mark = prompt_student_mark()
    if mark is None:
        print(f"{Style.DIM}Action cancelled. Returning to main menu.{Style.RESET}\n")
        return

    student = Student(name=name, mark=mark)
    students.append(student)
    print(
        f"{Style.GREEN}✓ Successfully added {student.name} | "
        f"Mark: {student.formatted_mark} | Grade: {student.grade}{Style.RESET}\n"
    )


def render_distribution_chart(marks: list[float]):
    """Renders a text-based ASCII bar chart showing grade frequencies."""
    grade_order = ["A", "B", "C", "D", "E"]
    counts = {g: 0 for g in grade_order}
    for m in marks:
        # Evaluate grade directly for histogram tally
        if m >= 90:
            counts["A"] += 1
        elif m >= 80:
            counts["B"] += 1
        elif m >= 70:
            counts["C"] += 1
        elif m >= 60:
            counts["D"] += 1
        else:
            counts["E"] += 1

    print(f"\n{Style.BOLD}Grade Distribution:{Style.RESET}")
    for grade in grade_order:
        tally = counts[grade]
        bar = "█" * (tally * 2) if tally > 0 else "·"
        print(f"  Grade {grade} [{tally:>2}]: {bar}")


def show_results():
    """Renders tabular report, class statistics, and visual frequency chart."""
    if not students:
        print(f"\n{Style.YELLOW}No student records found. Add students first.{Style.RESET}\n")
        return

    marks = [s.mark for s in students]
    highest = max(marks)
    lowest = min(marks)
    average = sum(marks) / len(marks)

    # Dynamic column width calculation to prevent layout breaks on long names
    max_name_len = max(len(s.name) for s in students)
    name_col_width = max(max_name_len + 2, 16)
    mark_w = 8
    grade_w = 8
    status_w = 10

    # Total inner content width: margins + 3 spaces between columns
    inner_width = name_col_width + mark_w + grade_w + status_w + 3
    
    # Outer box border
    top_border = "┌" + "─" * (inner_width + 2) + "┐"
    divider = "├" + "─" * (inner_width + 2) + "┤"
    bottom_border = "└" + "─" * (inner_width + 2) + "┘"

    print("\n" + f"{Style.BOLD}{top_border}{Style.RESET}")
    title = "ACADEMIC GRADE REPORT"
    print(f"{Style.BOLD}│ {title.center(inner_width)} │{Style.RESET}")
    print(f"{Style.BOLD}{divider}{Style.RESET}")

    # Header
    print(
        f"{Style.BOLD}│ "
        f"{'Name':<{name_col_width}} "
        f"{'Mark':<{mark_w}} "
        f"{'Grade':<{grade_w}} "
        f"{'Status':<{status_w}} │{Style.RESET}"
    )
    print(f"{divider}")

    # Data Rows
    for s in students:
        # 1. Determine plain-text badge first (for correct spacing)
        if s.mark == highest and len(students) > 1:
            raw_status = "★ High"
            status_color = Style.GREEN
        elif s.mark == lowest and len(students) > 1 and highest != lowest:
            raw_status = "▼ Low"
            status_color = Style.RED
        else:
            raw_status = ""
            status_color = Style.RESET

        # 2. Pad plain strings first so terminal widths stay perfectly aligned
        name_cell = f"{s.name:<{name_col_width}}"
        mark_cell = f"{s.formatted_mark:<{mark_w}}"
        grade_cell = f"{s.grade:<{grade_w}}"
        status_cell = f"{raw_status:<{status_w}}"

        # 3. Apply ANSI styles around the correctly-padded cells
        colored_grade = f"{s.grade_color}{grade_cell}{Style.RESET}"
        colored_status = f"{status_color}{status_cell}{Style.RESET}"

        print(f"│ {name_cell} {mark_cell} {colored_grade} {colored_status} │")

    print(f"{bottom_border}")

    # Class Metrics
    highest_str = f"{int(highest)}" if highest.is_integer() else f"{highest:.1f}"
    lowest_str = f"{int(lowest)}" if lowest.is_integer() else f"{lowest:.1f}"

    print(f"\n{Style.BOLD}Average:{Style.RESET} {average:.1f}")
    print(f"{Style.BOLD}Highest:{Style.RESET} {highest_str}   {Style.BOLD}Lowest:{Style.RESET} {lowest_str}")

    # Visual ASCII Histogram
    render_distribution_chart(marks)
    print()


def main():
    """Application entry and event loop."""
    while True:
        print(f"{Style.BOLD}Student Grade Manager{Style.RESET}")
        print("1. Add Student")
        print("2. Show Results")
        print("3. Quit")

        choice = input(f"{Style.CYAN}Select option (1-3): {Style.RESET}").strip()

        if choice == "1":
            add_student_entry()
        elif choice == "2":
            show_results()
        elif choice == "3":
            print(f"\n{Style.GREEN}Program closed. Have a great day!{Style.RESET}")
            sys.exit(0)
        else:
            print(f"{Style.RED}Invalid option. Please enter 1, 2, or 3.{Style.RESET}\n")


if __name__ == "__main__":
    main()