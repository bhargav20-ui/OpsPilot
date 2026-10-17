
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from opspilot.health_checker import check_website


class TestOpsPilot(unittest.TestCase):

    @patch("opspilot.health_checker.urllib.request.urlopen")
    def test_website_returns_online(self, mock_urlopen):
        response = MagicMock()
        response.status = 200
        mock_urlopen.return_value.__enter__.return_value = response

        result = check_website("https://example.com")

        self.assertIn("ONLINE (HTTP 200)", result)

    @patch("opspilot.health_checker.urllib.request.urlopen")
    def test_website_handles_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            "https://example.com",
            404,
            "Not Found",
            {},
            None,
        )

        result = check_website("https://example.com")

        self.assertIn("HTTP 404", result)

    @patch("opspilot.health_checker.urllib.request.urlopen")
    def test_website_handles_connection_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Connection failed")

        result = check_website("https://example.com")

        self.assertIn("CHECK FAILED", result)


if __name__ == "__main__":
    unittest.main()
