import unittest

from opspilot.alerts import build_alerts


class AlertTests(unittest.TestCase):
    def setUp(self):
        self.websites = [{"url": "https://example.com", "status": "online", "http_status": 200, "error": None}]

    def test_no_alerts_under_threshold(self):
        alerts = build_alerts({"cpu_percent": 20, "ram_percent": 40}, self.websites, 80, 85)
        self.assertEqual(alerts, [])

    def test_cpu_alert(self):
        alerts = build_alerts({"cpu_percent": 90, "ram_percent": 40}, self.websites, 80, 85)
        self.assertEqual(len(alerts), 1)
        self.assertIn("CPU", alerts[0]["message"])

    def test_ram_alert(self):
        alerts = build_alerts({"cpu_percent": 20, "ram_percent": 90}, self.websites, 80, 85)
        self.assertIn("RAM", alerts[0]["message"])

    def test_unreachable_website_is_critical(self):
        failed = [{"url": "https://example.com", "status": "unreachable", "http_status": None, "error": "timed out"}]
        alerts = build_alerts({"cpu_percent": 20, "ram_percent": 40}, failed, 80, 85)
        self.assertEqual(alerts[0]["severity"], "critical")


if __name__ == "__main__":
    unittest.main()
