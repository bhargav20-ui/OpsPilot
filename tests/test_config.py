import json
import tempfile
import unittest
from pathlib import Path

from opspilot.config import load_config


class ConfigTests(unittest.TestCase):
    def test_loads_valid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"websites": ["https://example.com"]}), encoding="utf-8")
            config = load_config(path)
            self.assertEqual(config.websites, ("https://example.com",))
            self.assertEqual(config.cpu_alert_threshold, 80.0)

    def test_rejects_invalid_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"websites": ["https://example.com"], "ram_alert_threshold": 150}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_config(path)

    def test_rejects_invalid_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"websites": ["example.com"]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
