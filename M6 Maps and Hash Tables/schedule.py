import csv
from typing import Dict, List

from schedule_item import ScheduleItem


class Schedule:
    "Stores and manages a collection of ScheduleItem objects in a dictionary. Keys are strings of the form Subject_Catalog_Section to demonstrate Python dictionary / hash table usage."

    def __init__(self) -> None:
        # Internal dictionary used as a hash table:
        # key (str) -> ScheduleItem
        self._items: Dict[str, ScheduleItem] = {}

    def add_entry(self, item: ScheduleItem) -> None:
        "Add or replace a ScheduleItem using its unique key."
        key = item.get_key()
        self._items[key] = item

    def load_from_csv(self, filename: str) -> None:
        "Load schedule data from a CSV file using csv.DictReader.Expects the CSV to contain the following columns: Subject, Catalog, Section, Component, Session, Units, TotEnrl, CapEnrl, Instructor."
        with open(filename, encoding="utf-8-sig", newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    subject = row["Subject"].strip()
                    catalog = row["Catalog"].strip()
                    section = row["Section"].strip()
                    component = row["Component"].strip()
                    session = row["Session"].strip()
                    units_str = row["Units"].strip()
                    tot_enrl_str = row["TotEnrl"].strip()
                    cap_enrl_str = row["CapEnrl"].strip()
                    instructor = row["Instructor"].strip()
                except KeyError:
                    # If headers do not match, raise a clear error.
                    raise KeyError(
                        "CSV file missing required columns."
                        "Check that your courses.csv file has the correct header names."
                    )

                # Convert numeric fields safely; treat empty strings as 0
                units = int(units_str) if units_str else 0
                tot_enrl = int(tot_enrl_str) if tot_enrl_str else 0
                cap_enrl = int(cap_enrl_str) if cap_enrl_str else 0

                item = ScheduleItem(
                    subject=subject,
                    catalog=catalog,
                    section=section,
                    component=component,
                    session=session,
                    units=units,
                    tot_enrl=tot_enrl,
                    cap_enrl=cap_enrl,
                    instructor=instructor,
                )
                self.add_entry(item)

    def print_header(self) -> None:
        "Print the header line for the schedule report."
        header = (
            f"{'Subject':<8}"
            f"{'Catalog':<8}"
            f"{'Section':<10}"
            f"{'Component':<10}"
            f"{'Session':<8}"
            f"{'Units':>6}"
            f"{'TotEnrl':>10}"
            f"{'CapEnrl':>10}  "
            f"Instructor"
        )
        print(header)
        print("-" * len(header))

    def print(self, items: List[ScheduleItem] | None = None) -> None:
        "Print a formatted schedule report. If 'items' is None, prints the entire schedule; otherwise prints only the given list of ScheduleItem objects."
        if items is None:
            items = list(self._items.values())

        if not items:
            print("No Matching Courses Found.")
            return

        self.print_header()
        for item in items:
            print(item.format_row())

    @property
    def items(self) -> Dict[str, ScheduleItem]:
        "Read-only access to the internal dictionary of schedule items."
        return self._items

    def find_by_subject(self, subject: str) -> List[ScheduleItem]:
        "Return all courses that match the given subject code. Uses a list comprehension to filter the dictionary values."
        subject_upper = subject.strip().upper()
        return [
            item
            for item in self._items.values()
            if item.subject.upper() == subject_upper
        ]

    def find_by_subject_catalog(self, subject: str, catalog: str) -> List[ScheduleItem]:
        "Return all courses that match the given subject and catalog number. Example: subject='BIO', catalog='141' "
        subject_upper = subject.strip().upper()
        catalog_str = str(catalog).strip()
        return [
            item
            for item in self._items.values()
            if item.subject.upper() == subject_upper
            and item.catalog == catalog_str
        ]

    def find_by_instructor_last_name(self, last_name: str) -> List[ScheduleItem]:
        "Return all courses taught by an instructor whose last name matches the given string. Assumes instructor names are stored in 'Last,First' format."
        last_upper = last_name.strip().upper()
        return [
            item
            for item in self._items.values()
            if item.instructor.upper().split(",")[0].strip().endswith(last_upper)
        ]