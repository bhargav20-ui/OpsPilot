# OpsPilot — System Automation & Monitoring Toolkit

OpsPilot is a configurable Python command-line toolkit for monitoring local system resources, checking website/API endpoint availability, recording operational events, raising rule-based alerts, and producing machine-readable reports.

## Features

- **System monitoring:** live CPU and RAM utilization, available/total memory, hostname, operating system, and local timestamp.
- **Website and API endpoint checks:** configurable HTTP/HTTPS GET checks, response status, latency measurement, finite request timeout, and handling of HTTP errors, timeouts, and connection failures. API checks currently test reachability and HTTP response, not business-level JSON correctness or authenticated workflows.
- **Rule-based alerts:** configurable CPU/RAM thresholds, warnings for HTTP errors, and critical alerts for unreachable endpoints.
- **Repeated execution:** one-shot mode or a configurable polling interval while the process remains running; Ctrl+C shuts it down cleanly.
- **Structured logging:** timestamps, severity, endpoint outcomes, alerts, cycle summaries, and unexpected errors. Logs rotate at 1 MB and retain up to three backups.
- **Log analysis:** summarize log levels, successful checks, HTTP errors, connection/timeout failures, alerts, unexpected cycle failures, and malformed lines.
- **Reporting:** timestamped JSON report per cycle plus append-only CSV history.
- **Configuration validation and automated tests:** invalid URLs, thresholds, intervals, and configuration files are rejected early; unit tests cover core behavior.

## Requirements

- Python 3.10+
- Windows, macOS, or Linux
- Internet access for live endpoint checks
- psutil runtime dependency; pytest is used for the test suite

## Quick start (Windows PowerShell)

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -e ".[test]"
    python main.py

If PowerShell blocks environment activation, use .\.venv\Scripts\python.exe to run the commands.

## Usage

    # Run one monitoring cycle
    python main.py

    # Show command options
    python main.py --help

    # Repeat checks every 60 seconds
    python main.py --interval 60

    # Use a custom JSON configuration
    python main.py --config .\config.json

    # Analyze the configured application log and exit
    python main.py --analyze-logs

    # Run automated tests
    python -m pytest -v

    # Standard-library test runner is also supported
    python -m unittest discover -v

A configured interval_seconds value of 0 runs once. Repeated execution requires an interval of at least 5 seconds. The process must remain running for recurring checks; OpsPilot is not installed as an operating-system service and will not keep running after the terminal closes.

## Configuration

Edit config.json to choose URLs/endpoints, thresholds, timeouts, report output, logging output, and polling interval.

    {
      "websites": [
        "https://www.google.com",
        "https://github.com",
        "https://www.python.org"
      ],
      "cpu_alert_threshold": 80.0,
      "ram_alert_threshold": 85.0,
      "request_timeout_seconds": 8,
      "report_directory": "reports",
      "log_file": "logs/opspilot.log",
      "user_agent": "OpsPilot/1.0",
      "interval_seconds": 0
    }

For an API endpoint, add its full URL to the websites list, for example https://api.github.com/. This version checks HTTP reachability and status codes; it does not authenticate to private APIs or validate response payload schemas.

## Output

- reports/report_<timestamp>.json — system snapshot, endpoint results, alerts, and summary for each cycle.
- reports/history.csv — one compact summary row per cycle.
- logs/opspilot.log — rotating operational log used by the log-analysis command.

Generated reports and logs are local runtime artifacts and should not be committed.

## Continuous integration

GitHub Actions runs the pytest suite on pushes and pull requests using Python 3.10, 3.11, and 3.12.

## Project structure

    OpsPilot/
    ├── main.py
    ├── config.json
    ├── requirements.txt
    ├── pyproject.toml
    ├── opspilot/
    │   ├── cli.py
    │   ├── config.py
    │   ├── system_monitor.py
    │   ├── health_checker.py
    │   ├── alerts.py
    │   ├── reporter.py
    │   ├── logging_config.py
    │   └── log_analyzer.py
    ├── tests/
    └── .github/workflows/tests.yml

## Scope and limitations

OpsPilot is a local monitoring CLI, not a hosted monitoring service. Recurring checks run only while the program is running. Alerts are currently written to the console and application log; email/SMS delivery, a web dashboard, operating-system background-service installation, authenticated API workflows, and application-specific payload validation are not included. An HTTP success indicates that an endpoint responded successfully, not that every feature of the remote application is healthy.

## Security

Only configure endpoints you are authorized to monitor. Do not put credentials, tokens, or other secrets in config.json. This version uses unauthenticated GET requests.
