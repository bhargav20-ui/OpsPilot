
import unittest
from opspilot.alerts import check_website_alerts
from opspilot.alerts import check_resource_alerts


class TestResourceAlerts(unittest.TestCase):

    def test_high_cpu_triggers_alert(self):
        metrics = {
            "cpu_usage": 95.0,
            "ram_usage": 50.0,
        }

        alerts = check_resource_alerts(metrics)

        self.assertTrue(any("CPU usage is high" in alert for alert in alerts))

    def test_high_ram_triggers_alert(self):
        metrics = {
            "cpu_usage": 30.0,
            "ram_usage": 92.0,
        }

        alerts = check_resource_alerts(metrics)

        self.assertTrue(any("RAM usage is high" in alert for alert in alerts))

    def test_normal_usage_has_no_warning(self):
        metrics = {
            "cpu_usage": 30.0,
            "ram_usage": 50.0,
        }

        alerts = check_resource_alerts(metrics)

        self.assertEqual(len(alerts), 1)
        self.assertIn("within configured thresholds", alerts[0])

    def test_both_resources_trigger_alerts(self):
        metrics = {
            "cpu_usage": 95.0,
            "ram_usage": 92.0,
        }

        alerts = check_resource_alerts(metrics)

        self.assertEqual(len(alerts), 2)


class TestWebsiteAlerts(unittest.TestCase):

    def test_online_website_does_not_trigger_alert(self):
        results = {
            "https://example.com": "ONLINE (HTTP 200) | Response: 20 ms",
        }

        alerts = check_website_alerts(results)

        self.assertEqual(alerts, [])

    def test_connection_failure_triggers_alert(self):
        results = {
            "https://broken.example": "CHECK FAILED | Connection error",
        }

        alerts = check_website_alerts(results)

        self.assertEqual(len(alerts), 1)
        self.assertIn("https://broken.example", alerts[0])

    def test_http_error_triggers_alert(self):
        results = {
            "https://missing.example": "SERVER RESPONDED (HTTP 404)",
        }

        alerts = check_website_alerts(results)

        self.assertEqual(len(alerts), 1)
        self.assertIn("HTTP 404", alerts[0])



if __name__ == "__main__":
    unittest.main()
