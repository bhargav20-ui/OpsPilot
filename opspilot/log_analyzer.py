"""Analyze OpsPilot's structured application log."""
from __future__ import annotations

from collections import Counter
from pathlib import Path


def analyze_logs(log_file: str | Path = "logs/opspilot.log") -> dict:
    """Count valid structured log records and classify monitoring outcomes."""
    path = Path(log_file)
    summary = {
        "log_file": str(path), "total_entries": 0, "levels": {},
        "website_successes": 0, "http_errors": 0, "check_failures": 0,
        "alerts": 0, "cycle_failures": 0, "malformed_lines": 0,
    }
    if not path.exists():
        summary["missing_file"] = True
        return summary
    levels: Counter[str] = Counter()
    with path.open("r", encoding="utf-8", errors="replace") as file:
        for line in file:
            line = line.rstrip("\r\n")
            if not line:
                continue
            parts = line.split(" | ", 3)
            if len(parts) != 4:
                summary["malformed_lines"] += 1
                continue
            level, message = parts[1], parts[3]
            levels[level] += 1
            summary["total_entries"] += 1
            if "Website check succeeded:" in message:
                summary["website_successes"] += 1
            elif "Website returned HTTP error:" in message:
                summary["http_errors"] += 1
            elif "Website check failed:" in message:
                summary["check_failures"] += 1
            if "Alert:" in message:
                summary["alerts"] += 1
            if "Unexpected monitoring cycle failure" in message:
                summary["cycle_failures"] += 1
    summary["levels"] = dict(sorted(levels.items()))
    summary["missing_file"] = False
    return summary


def display_log_summary(summary: dict) -> None:
    """Print a human-readable log analysis report."""
    print("\n" + "=" * 48)
    print("                 OpsPilot Log Analysis")
    print("=" * 48)
    print(f"Log file: {summary['log_file']}")
    if summary.get("missing_file"):
        print("No log file exists yet. Run a monitoring cycle first.")
        return
    print(f"Structured log entries: {summary['total_entries']}")
    print(f"Entries by level: {summary['levels']}")
    print(f"Successful endpoint checks: {summary['website_successes']}")
    print(f"HTTP error responses: {summary['http_errors']}")
    print(f"Connection/timeout failures: {summary['check_failures']}")
    print(f"Recorded alerts: {summary['alerts']}")
    print(f"Unexpected cycle failures: {summary['cycle_failures']}")
    print(f"Malformed non-empty lines skipped: {summary['malformed_lines']}")
