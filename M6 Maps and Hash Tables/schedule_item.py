from dataclasses import dataclass

@dataclass
class ScheduleItem:
    "Represents a single course in the schedule."
    subject: str
    catalog: str
    section: str
    component: str
    session: str
    units: int
    tot_enrl: int
    cap_enrl: int
    instructor: str

    def get_key(self) -> str:
        "Build a unique hash key for this course to be used in the dictionary. Format: Subject_Catalog_Section"
        return f"{self.subject}_{self.catalog}_{self.section}"

    def format_row(self) -> str:
        "Return a formatted string for printing this item in a tabular report."
        return (
            f"{self.subject:<8}"
            f"{self.catalog:<8}"
            f"{self.section:<10}"
            f"{self.component:<10}"
            f"{self.session:<8}"
            f"{self.units:>6}"
            f"{self.tot_enrl:>10}"
            f"{self.cap_enrl:>10}  "
            f"{self.instructor}"
        )