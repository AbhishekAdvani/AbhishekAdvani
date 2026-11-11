"""Update the age marker in the profile README from the November 18 birthday."""

from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
BIRTH_DATE = (2000, 11, 18)
TIMEZONE = ZoneInfo("Asia/Kolkata")


def age_on(today: date) -> int:
    year, month, day = BIRTH_DATE
    return today.year - year - ((today.month, today.day) < (month, day))


def main() -> None:
    today = datetime.now(TIMEZONE).date()
    readme = README.read_text()
    start = "<!-- AGE -->"
    end = "<!-- /AGE -->"
    before, marker, remainder = readme.partition(start)
    if not marker:
        raise SystemExit("README is missing the age marker start.")
    current, closing, after = remainder.partition(end)
    if not closing:
        raise SystemExit("README is missing the age marker end.")

    updated = f"{before}{start}{age_on(today)}{end}{after}"
    if updated != readme:
        README.write_text(updated)


if __name__ == "__main__":
    main()
