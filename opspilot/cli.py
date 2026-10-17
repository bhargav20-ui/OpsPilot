"""CLI orchestration, scheduling, reporting, and log analysis."""
from __future__ import annotations

import argparse
import time
from collections import Counter
from pathlib import Path

from opspilot.alerts import build_alerts
from opspilot.config import load_config
from opspilot.health_checker import check_website
from opspilot.logging_config import configure_logging
from opspilot.log_analyzer import analyze_logs, display_log_summary
from opspilot.reporter import save_report
from opspilot.system_monitor import get_system_metrics


def run_cycle(config, logger) -> Path:
    """Run one monitoring cycle, log each check, and persist its report."""
    metrics = get_system_metrics()
    website_results = [
        check_website(url, config.request_timeout_seconds, config.user_agent)
        for url in config.websites
    ]
    for result in website_results:
        if result["status"] == "online":
            logger.info("Website check succeeded: %s status=%s latency_ms=%.2f",
                        result["url"], result["http_status"], result["response_time_ms"])
        elif result["status"] == "http_error":
            logger.warning("Website returned HTTP error: %s status=%s latency_ms=%.2f",
                           result["url"], result["http_status"], result["response_time_ms"])
        else:
            logger.error("Website check failed: %s error=%s latency_ms=%.2f",
                         result["url"], result["error"], result["response_time_ms"])

    alerts = build_alerts(metrics, website_results, config.cpu_alert_threshold, config.ram_alert_threshold)
    counts = Counter(result["status"] for result in website_results)
    report = {
        "application": {"name": "OpsPilot", "version": "1.1.0"},
        "system": metrics,
        "websites": website_results,
        "alerts": alerts,
        "summary": {
            "websites_checked": len(website_results),
            "websites_online": counts.get("online", 0),
            "websites_with_issues": len(website_results) - counts.get("online", 0),
            "alert_count": len(alerts),
        },
    }
    print("\n" + "=" * 58)
    print("                         OpsPilot")
    print("=" * 58)
    print(f"Time: {metrics['timestamp']}")
    print(f"Computer: {metrics['hostname']} | OS: {metrics['operating_system']}")
    print(f"CPU: {metrics['cpu_percent']:.1f}% | RAM: {metrics['ram_percent']:.1f}% "
          f"({metrics['available_ram_gb']:.2f} GB available / {metrics['total_ram_gb']:.2f} GB)")
    print("\nWebsite/API endpoint health")
    for result in website_results:
        status_code = f"HTTP {result['http_status']}" if result["http_status"] is not None else result["status"].upper()
        extra = f" — {result['error']}" if result["error"] else ""
        print(f"  {result['status'].upper():12} {result['url']} | {status_code} | "
              f"{result['response_time_ms']:.2f} ms{extra}")
    print("\nAlerts")
    for alert in alerts:
        print(f"  [{alert['severity'].upper()}] {alert['message']}")
    if not alerts:
        print("  No alerts. All configured checks are within expected limits.")

    report_path = save_report(report, config.report_directory)
    print("\nSummary")
    print(f"  Websites/endpoints online: {counts.get('online', 0)}/{len(website_results)}")
    print(f"  Alerts: {len(alerts)}")
    print(f"  JSON report: {report_path}")
    print(f"  CSV history: {Path(config.report_directory) / 'history.csv'}")
    logger.info("Cycle completed: websites=%d online=%d issues=%d alerts=%d report=%s",
                len(website_results), counts.get("online", 0),
                len(website_results) - counts.get("online", 0), len(alerts), report_path)
    for alert in alerts:
        level = logger.error if alert["severity"] == "critical" else logger.warning
        level("Alert: %s", alert["message"])
    return report_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor CPU/RAM usage and configured website or API endpoints.")
    parser.add_argument("--config", default="config.json", help="Path to JSON configuration (default: config.json)")
    parser.add_argument("--interval", type=int, default=None,
                        help="Repeat interval in seconds; overrides config. Minimum 5. Omit/0 to run once.")
    parser.add_argument("--analyze-logs", action="store_true",
                        help="Summarize the configured application log and exit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
        interval = config.interval_seconds if args.interval is None else args.interval
        if interval < 0 or 0 < interval < 5:
            raise ValueError("interval must be 0 or at least 5 seconds")
        logger = configure_logging(config.log_file)
    except (ValueError, OSError) as exc:
        print(f"Configuration error: {exc}")
        return 2
    if args.analyze_logs:
        display_log_summary(analyze_logs(config.log_file))
        return 0
    try:
        while True:
            run_cycle(config, logger)
            if interval == 0:
                return 0
            print(f"\nNext cycle in {interval} seconds. Press Ctrl+C to stop.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nOpsPilot stopped by user.")
        logger.info("Monitoring stopped by user")
        return 0
    except Exception:
        logger.exception("Unexpected monitoring cycle failure")
        print("An unexpected error occurred. Check the log file for details.")
        return 1
