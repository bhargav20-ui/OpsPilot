
"""Alerting functions for OpsPilot."""

from opspilot.config import (
    CPU_ALERT_THRESHOLD,
    RAM_ALERT_THRESHOLD,
)


def check_resource_alerts(metrics):
    """Return alerts when CPU or RAM usage reaches its threshold."""
    alerts = []

    cpu_usage = metrics["cpu_usage"]
    ram_usage = metrics["ram_usage"]

    if cpu_usage >= CPU_ALERT_THRESHOLD:
        alerts.append(
            f"WARNING: CPU usage is high ({cpu_usage}%). "
            f"Threshold: {CPU_ALERT_THRESHOLD}%."
        )

    if ram_usage >= RAM_ALERT_THRESHOLD:
        alerts.append(
            f"WARNING: RAM usage is high ({ram_usage}%). "
            f"Threshold: {RAM_ALERT_THRESHOLD}%."
        )

    if not alerts:
        alerts.append("System resource usage is within configured thresholds.")

    return alerts


def display_resource_alerts(metrics):
    """Print resource alerts in a readable format."""
    print("\n" + "=" * 45)
    print("             Resource Alerts")
    print("=" * 45)

    for alert in check_resource_alerts(metrics):
        print(alert)


def check_website_alerts(website_results):
    """Return alerts for websites that are not fully online."""
    alerts = []

    for url, result in website_results.items():
        if "ONLINE (HTTP" not in result:
            alerts.append(
                f"WARNING: Website health check needs attention: "
                f"{url} — {result}"
            )

    return alerts
