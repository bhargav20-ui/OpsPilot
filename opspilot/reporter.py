"""Write durable JSON reports and an append-only CSV history."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from datetime import datetime


def save_report(report: dict, report_directory: str | Path) -> Path:
    directory = Path(report_directory)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    report_path = directory / f"report_{timestamp}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    history_path = directory / "history.csv"
    fields = [
        "timestamp", "hostname", "cpu_percent", "ram_percent",
        "websites_checked", "websites_online", "websites_with_issues", "alert_count",
    ]
    summary = report["summary"]
    row = {
        "timestamp": report["system"]["timestamp"],
        "hostname": report["system"]["hostname"],
        "cpu_percent": report["system"]["cpu_percent"],
        "ram_percent": report["system"]["ram_percent"],
        "websites_checked": summary["websites_checked"],
        "websites_online": summary["websites_online"],
        "websites_with_issues": summary["websites_with_issues"],
        "alert_count": summary["alert_count"],
    }
    is_new = not history_path.exists() or history_path.stat().st_size == 0
    with history_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if is_new:
            writer.writeheader()
        writer.writerow(row)
    return report_path
