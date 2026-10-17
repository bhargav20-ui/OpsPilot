"""Load and validate OpsPilot configuration."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AppConfig:
    websites: tuple[str, ...]
    cpu_alert_threshold: float = 80.0
    ram_alert_threshold: float = 85.0
    request_timeout_seconds: float = 8.0
    report_directory: str = "reports"
    log_file: str = "logs/opspilot.log"
    user_agent: str = "OpsPilot/1.0"
    interval_seconds: int = 0


def _number(data: dict[str, Any], key: str, default: float) -> float:
    value = data.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a number")
    return float(value)


def load_config(path: str | Path = "config.json") -> AppConfig:
    """Read JSON configuration and reject invalid settings early."""
    config_path = Path(path)
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Configuration file not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in configuration file: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Configuration root must be a JSON object")

    websites = data.get("websites")
    if not isinstance(websites, list) or not websites:
        raise ValueError("'websites' must be a non-empty list of URLs")
    clean_websites = []
    for url in websites:
        if not isinstance(url, str):
            raise ValueError("Every website URL must be a string")
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            raise ValueError(f"Website URL must start with http:// or https://: {url!r}")
        clean_websites.append(url)

    cpu = _number(data, "cpu_alert_threshold", 80.0)
    ram = _number(data, "ram_alert_threshold", 85.0)
    timeout = _number(data, "request_timeout_seconds", 8.0)
    interval_raw = data.get("interval_seconds", 0)
    if isinstance(interval_raw, bool) or not isinstance(interval_raw, int):
        raise ValueError("interval_seconds must be an integer")
    if not 0 <= cpu <= 100 or not 0 <= ram <= 100:
        raise ValueError("CPU and RAM thresholds must be between 0 and 100")
    if timeout <= 0:
        raise ValueError("request_timeout_seconds must be greater than 0")
    if interval_raw < 0 or 0 < interval_raw < 5:
        raise ValueError("interval_seconds must be 0 or at least 5")

    report_directory = data.get("report_directory", "reports")
    log_file = data.get("log_file", "logs/opspilot.log")
    user_agent = data.get("user_agent", "OpsPilot/1.0")
    for key, value in (("report_directory", report_directory), ("log_file", log_file), ("user_agent", user_agent)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")

    return AppConfig(
        websites=tuple(clean_websites),
        cpu_alert_threshold=cpu,
        ram_alert_threshold=ram,
        request_timeout_seconds=timeout,
        report_directory=report_directory,
        log_file=log_file,
        user_agent=user_agent,
        interval_seconds=interval_raw,
    )
