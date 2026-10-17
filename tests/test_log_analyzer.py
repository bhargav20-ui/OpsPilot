import tempfile
import unittest
from pathlib import Path

from opspilot.log_analyzer import analyze_logs


class LogAnalyzerTests(unittest.TestCase):
    def test_missing_log_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = analyze_logs(Path(tmp) / "missing.log")
        self.assertTrue(summary["missing_file"])
        self.assertEqual(summary["total_entries"], 0)

    def test_counts_structured_monitoring_events(self):
        content = (
            "2026-10-17 10:00:00,000 | INFO | opspilot | Website check succeeded: https://example.com status=200 latency_ms=20\n"
            "2026-10-17 10:00:01,000 | WARNING | opspilot | Website returned HTTP error: https://bad.example status=503 latency_ms=30\n"
            "2026-10-17 10:00:02,000 | ERROR | opspilot | Website check failed: https://down.example error=timeout latency_ms=40\n"
            "2026-10-17 10:00:03,000 | WARNING | opspilot | Alert: RAM usage is high\n"
            "not a structured record\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "opspilot.log"
            path.write_text(content, encoding="utf-8")
            summary = analyze_logs(path)
        self.assertEqual(summary["total_entries"], 4)
        self.assertEqual(summary["website_successes"], 1)
        self.assertEqual(summary["http_errors"], 1)
        self.assertEqual(summary["check_failures"], 1)
        self.assertEqual(summary["alerts"], 1)
        self.assertEqual(summary["malformed_lines"], 1)
        self.assertEqual(summary["levels"], {"ERROR": 1, "INFO": 1, "WARNING": 2})


if __name__ == "__main__":
    unittest.main()
