
import argparse
import time

from opspilot.config import WEBSITES
from opspilot.alerts import (
    display_resource_alerts,
    check_website_alerts,
)
from opspilot.log_analyzer import analyze_logs, display_log_summary
from opspilot.system_monitor import (
    get_system_metrics,
    display_system_metrics,
)
from opspilot.health_checker import check_website
from opspilot.reporter import save_report


def main():
    """Run one OpsPilot monitoring cycle."""

    # Collect and display system metrics.
    metrics = get_system_metrics()
    display_system_metrics(metrics)
    display_resource_alerts(metrics)

    # Check configured websites.
    print("\n" + "=" * 45)
    print("           Website Health Checks")
    print("=" * 45)

    website_results = {}

    for website in WEBSITES:
        website_results[website] = check_website(website)

    # Display alerts for website health issues.
    website_alerts = check_website_alerts(website_results)

    print("\n" + "=" * 45)
    print("             Website Alerts")
    print("=" * 45)

    if website_alerts:
        for alert in website_alerts:
            print(alert)
    else:
        print("All configured websites are responding successfully.")

    # Display a health summary.
    online = sum(
        "ONLINE (HTTP" in result
        for result in website_results.values()
    )
    responded = sum(
        "SERVER RESPONDED" in result
        for result in website_results.values()
    )
    failed = len(website_results) - online - responded

    print("\n" + "=" * 45)
    print("             Health Summary")
    print("=" * 45)
    print(f"Online: {online}")
    print(f"Server responded with an HTTP error: {responded}")
    print(f"Check failed: {failed}")
    print(f"Total checked: {len(website_results)}")

    # Save the monitoring report.
    report_file = save_report(metrics, website_results)

    print("\n" + "=" * 45)
    print("          Monitoring Complete")
    print(f"Report saved: {report_file}")
    print("=" * 45)

    # Analyze historical log activity.
    log_summary = analyze_logs()
    display_log_summary(log_summary)


def parse_args():
    """Parse optional monitoring schedule settings."""

    parser = argparse.ArgumentParser(
        description="OpsPilot system monitor"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=0,
        help="Repeat monitoring every N seconds; 0 runs once.",
    )

    args = parser.parse_args()

    if args.interval < 0:
        parser.error("--interval must be 0 or greater")

    if 0 < args.interval < 5:
        parser.error("--interval must be at least 5 seconds")

    return args


def run_monitoring():
    """Run once or repeat monitoring at the requested interval."""

    args = parse_args()

    try:
        while True:
            main()

            if args.interval == 0:
                break

            print(
                f"\nNext monitoring cycle in {args.interval} seconds. "
                "Press Ctrl+C to stop."
            )
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nOpsPilot monitoring stopped by user.")


if __name__ == "__main__":
    run_monitoring()
