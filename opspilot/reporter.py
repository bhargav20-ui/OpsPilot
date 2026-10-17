
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"


def save_report(system_metrics, website_results):
    """Save system metrics and website health results to a text report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now()
    report_lines = [
        "OpsPilot Monitoring Report",
        "=" * 45,
        f"Timestamp: {timestamp:%Y-%m-%d %H:%M:%S}",
        f"Computer: {system_metrics['computer']}",
        f"Operating System: {system_metrics['operating_system']}",
        f"CPU Usage: {system_metrics['cpu_usage']}%",
        f"RAM Usage: {system_metrics['ram_usage']}%",
        f"Available RAM: {system_metrics['available_ram_gb']:.2f} GB",
        "",
        "Website Health Checks",
        "-" * 45,
    ]

    online_count = 0
    responded_count = 0
    failed_count = 0

    for url, result in website_results.items():
        report_lines.append(f"{url}: {result}")

        if "ONLINE (HTTP" in result:
            online_count += 1
        elif "SERVER RESPONDED" in result:
            responded_count += 1
        else:
            failed_count += 1

    report_lines.extend([
        "",
        "Health Summary",
        "-" * 45,
        f"Online: {online_count}",
        f"Server responded with an HTTP error: {responded_count}",
        f"Check failed: {failed_count}",
        f"Total checked: {len(website_results)}",
    ])

    report_file = REPORT_DIR / (
        f"report_{timestamp:%Y%m%d_%H%M%S_%f}.txt"
    )

    report_file.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    return report_file
