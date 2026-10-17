import csv
import json
import tempfile
import unittest
from pathlib import Path

from opspilot.reporter import save_report


class ReporterTests(unittest.TestCase):
    def test_writes_json_and_csv_history(self):
        report = {
            "system": {
                "timestamp": "2026-01-01T12:00:00+05:30",
                "hostname": "test-machine",
                "cpu_percent": 12.0,
                "ram_percent": 34.0,
            },
            "summary": {
                "websites_checked": 2,
                "websites_online": 1,
                "websites_with_issues": 1,
                "alert_count": 1,
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = save_report(report, tmp)
            self.assertTrue(path.exists())
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["summary"]["alert_count"], 1)
            with (Path(tmp) / "history.csv").open(encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["websites_online"], "1")


if __name__ == "__main__":
    unittest.main()
