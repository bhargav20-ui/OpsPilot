
from collections import Counter
from pathlib import Path

from opspilot.logger_config import LOG_FILE


def analyze_logs(log_file=LOG_FILE):
    """Count log levels and summarize recorded website checks."""
    path = Path(log_file)

    if not path.exists():
        return {
            "total_entries": 0,
            "levels": {},
            "website_successes": 0,
            "http_errors": 0,
            "check_failures": 0,
        }

    levels = Counter()
    website_successes = 0
    http_errors = 0
    check_failures = 0
    total_entries = 0

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if " | " not in line:
                continue

            parts = line.split(" | ", 3)
            if len(parts) < 4:
                continue

            level = parts[1]
            message = parts[3]

            levels[level] += 1
            total_entries += 1

            if "Website check succeeded" in message:
                website_successes += 1
            elif "Website returned HTTP error" in message:
                http_errors += 1
            elif "Website check failed" in message:
                check_failures += 1

    return {
        "total_entries": total_entries,
        "levels": dict(levels),
        "website_successes": website_successes,
        "http_errors": http_errors,
        "check_failures": check_failures,
    }


def display_log_summary(summary):
    """Display a readable summary of log activity."""
    print("\n" + "=" * 45)
    print("             OpsPilot Log Analysis")
    print("=" * 45)
    print(f"Total log entries: {summary['total_entries']}")
    print(f"Log levels: {summary['levels']}")
    print(f"Successful website checks: {summary['website_successes']}")
    print(f"HTTP errors: {summary['http_errors']}")
    print(f"Check failures: {summary['check_failures']}")
