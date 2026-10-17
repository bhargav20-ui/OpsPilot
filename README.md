
# OpsPilot

OpsPilot is a lightweight Python-based system monitoring and website health-check tool. It monitors CPU and RAM usage, checks website availability, generates reports, and analyzes historical application logs.

## Features

- Displays operating system, computer name, and monitoring timestamp.
- Monitors CPU usage, RAM usage, and available memory.
- Generates resource warnings when CPU or RAM usage reaches configured thresholds.
- Checks configured websites for availability using HTTP requests.
- Measures website response time.
- Distinguishes successful HTTP responses, HTTP errors, and connection failures.
- Generates timestamped text reports.
- Logs monitoring events for later analysis.
- Analyzes historical logs, including log levels and website-check outcomes.
- Supports one-time and recurring monitoring through a configurable interval.
- Includes automated unit tests for website checks and alert logic.
- Handles Ctrl+C to stop recurring monitoring gracefully.

## Technologies Used

- Python
- psutil
- urllib
- argparse
- unittest
- Python logging

## Requirements

- Python 3.10 or newer
- Internet connection for live website checks

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Configuration

Edit `opspilot/config.py` to configure the websites to monitor and the resource alert thresholds.

Example:

```python
WEBSITES = [
    "https://www.google.com",
    "https://github.com",
    "https://www.python.org",
]

CPU_ALERT_THRESHOLD = 80.0
RAM_ALERT_THRESHOLD = 85.0
```

Thresholds are expressed as percentages.

## Usage

### Run monitoring once

```powershell
python main.py
```

### Display command-line help

```powershell
python main.py --help
```

### Run monitoring repeatedly

Set the interval between monitoring cycles in seconds:

```powershell
python main.py --interval 10
```

This runs a monitoring cycle, waits 10 seconds, and then starts the next cycle. The interval must be at least 5 seconds.

Press `Ctrl+C` to stop recurring monitoring.

## Reports and Logs

- `reports/` stores generated timestamped text reports.
- `logs/opspilot.log` stores application log entries used for historical log analysis.

The log summary reports total entries, log-level counts, and website-check outcomes recorded in the logs. Historical failures may include earlier checks or test-generated events, not only the latest monitoring cycle.

## Run Tests

Run the complete test suite:

```powershell
python -m unittest discover -v
```

The tests cover website-check outcomes and resource and website alert logic. Website-check tests use mocked responses for the scenarios they test, so those tests do not require live website access.

## Project Structure

```text
OpsPilot/
├── main.py
├── main_backup.py
├── opspilot/
│   ├── __init__.py
│   ├── config.py
│   ├── system_monitor.py
│   ├── health_checker.py
│   ├── alerts.py
│   ├── reporter.py
│   ├── logger_config.py
│   └── log_analyzer.py
├── tests/
│   ├── __init__.py
│   └── test_alerts.py
├── test_main.py
├── requirements.txt
├── reports/
├── logs/
├── .gitignore
└── README.md
```

The `.venv/` directory and generated files should generally remain local and should not be committed to Git. The structure above describes the main project files; additional local files may exist.

## Future Improvements

- Export reports in CSV or JSON format.
- Add a dashboard for viewing monitoring results.
- Add optional notification channels.
- Expand test coverage for reporting, configuration, and log analysis.

## Disclaimer

OpsPilot is an educational monitoring project. Website availability and response times may vary depending on network conditions and server behavior.
