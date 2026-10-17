import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from opspilot.health_checker import check_website


class HealthCheckerTests(unittest.TestCase):
    @patch("opspilot.health_checker.urlopen")
    def test_online(self, mocked_urlopen):
        response = MagicMock()
        response.status = 200
        response.__enter__.return_value = response
        mocked_urlopen.return_value = response
        result = check_website("https://example.com")
        self.assertEqual(result["status"], "online")
        self.assertEqual(result["http_status"], 200)
        self.assertIsNone(result["error"])

    @patch("opspilot.health_checker.urlopen", side_effect=HTTPError("https://example.com", 503, "Unavailable", {}, None))
    def test_http_error(self, _mocked):
        result = check_website("https://example.com")
        self.assertEqual(result["status"], "http_error")
        self.assertEqual(result["http_status"], 503)

    @patch("opspilot.health_checker.urlopen", side_effect=URLError("connection failed"))
    def test_unreachable(self, _mocked):
        result = check_website("https://example.com")
        self.assertEqual(result["status"], "unreachable")
        self.assertIsNone(result["http_status"])
        self.assertIn("connection failed", result["error"])

    @patch("opspilot.health_checker.urlopen", side_effect=TimeoutError("timed out"))
    def test_timeout(self, _mocked):
        result = check_website("https://example.com", timeout=1)
        self.assertEqual(result["status"], "unreachable")
        self.assertIn("timed out", result["error"])


if __name__ == "__main__":
    unittest.main()
