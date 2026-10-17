# OpsPilot

OpsPilot is a configurable Python monitoring CLI for local system resources and website availability. It collects live CPU/RAM metrics, checks configured HTTP endpoints, evaluates alert thresholds, emits timestamped JSON reports, appends CSV history, and records operational logs.

## Features

- Live CPU, memory, hostname, OS, and timestamp metrics (`psutil`)
- Configurable websites, resource thresholds, request timeout, and polling interval
- HTTP status classification, latency measurement, and connection/timeout error handling
- Console resource and website alerts
- Timestamped JSON report per monitoring cycle
- Append-only CSV summary history
- Rotating application log file
- One-shot mode or repeated polling with graceful Ctrl+C shutdown
- Configuration validation and 10+ unit tests using mocked network/system responses

## Requirements

- Python 3.10+
- Internet access for live website checks
- Windows, macOS, or Linux

## Quick start (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` instead of `python` for the commands below.

## Run modes

```powershell
# One monitoring cycle
python main.py

# Print CLI options
python main.py --help

# Repeat every 60 seconds (minimum interval: 5 seconds)
python main.py --interval 60

# Use another JSON configuration file
python main.py --config .\config.json

# Override the configured interval for this run
python main.py --interval 30
```

Press `Ctrl+C` to stop recurring monitoring. The process only monitors while it is running; it is not installed as an operating-system service.

## Configuration

Edit `config.json`. Website URLs and thresholds are configuration, not embedded in the monitoring logic.

```json
{
  "websites": ["https://example.com", "https://www.python.org"],
  "cpu_alert_threshold": 80.0,
  "ram_alert_threshold": 85.0,
  "request_timeout_seconds": 8,
  "report_directory": "reports",
  "log_file": "logs/opspilot.log",
  "user_agent": "OpsPilot/1.0",
  "interval_seconds": 0
}
```

Thresholds are percentages from 0 to 100. `interval_seconds: 0` runs once. A repeating interval must be at least 5 seconds. Website checks use a finite timeout.

## Output

- `reports/report_<timestamp>.json`: detailed metrics, website outcomes, alerts, and summary for one cycle
- `reports/history.csv`: one compact row per cycle
- `logs/opspilot.log`: rotating application log

Generated reports and logs are ignored by Git. Historical logs can include earlier failures; read them as history, not as the status of the latest cycle.

## Tests

```powershell
python -m unittest discover -v
```

Tests use mocks for network and system data, so they do not depend on live websites.

## Project layout

```text
OpsPilot/
├── main.py
├── config.json
├── requirements.txt
├── pyproject.toml
├── opspilot/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── system_monitor.py
│   ├── health_checker.py
│   ├── alerts.py
│   ├── reporter.py
│   └── logging_config.py
└── tests/
    ├── __init__.py
    ├── test_config.py
    ├── test_health_checker.py
    ├── test_alerts.py
    └── test_reporter.py
```

## Scope and limitations

OpsPilot is a local monitoring CLI, not a hosted SaaS monitoring service. It does not currently send email/SMS notifications, run as a background service after the terminal closes, or provide a web dashboard. Website availability checks indicate whether a URL responded to a request from this machine; they do not guarantee full application health.

## Security note

Only configure URLs you are authorized to monitor. Keep credentials and secrets out of `config.json`; this version does not need credentials.
