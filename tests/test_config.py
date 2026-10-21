import json
import tempfile
import unittest
from pathlib import Path

from opspilot.config import load_config


class ConfigTests(unittest.TestCase):
    def _load(self, config_data):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        path = Path(temporary_directory.name) / "config.json"
        path.write_text(json.dumps(config_data), encoding="utf-8")
        return load_config(path)

    def test_loads_valid_config(self):
        config = self._load({"websites": ["https://example.com"]})
        self.assertEqual(config.websites, ("https://example.com",))
        self.assertEqual(config.cpu_alert_threshold, 80.0)

    def test_rejects_invalid_threshold(self):
        with self.assertRaises(ValueError):
            self._load({"websites": ["https://example.com"], "ram_alert_threshold": 150})

    def test_rejects_url_without_scheme(self):
        with self.assertRaises(ValueError):
            self._load({"websites": ["example.com"]})

    def test_rejects_url_without_hostname(self):
        for url in ("https://", "http:///path", "https://?query=value"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self._load({"websites": [url]})

    def test_rejects_unsupported_scheme(self):
        with self.assertRaises(ValueError):
            self._load({"websites": ["ftp://example.com"]})

    def test_rejects_malformed_or_out_of_range_port(self):
        for url in ("https://example.com:not-a-port", "https://example.com:70000"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self._load({"websites": [url]})

    def test_rejects_embedded_credentials(self):
        with self.assertRaises(ValueError):
            self._load({"websites": ["https://user:password@example.com"]})

    def test_rejects_whitespace_inside_url(self):
        with self.assertRaises(ValueError):
            self._load({"websites": ["https://exa mple.com"]})


if __name__ == "__main__":
    unittest.main()
