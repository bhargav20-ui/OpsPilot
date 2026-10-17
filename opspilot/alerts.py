"""Rule-based alerts for system resources and website checks."""
from __future__ import annotations


def build_alerts(metrics: dict, website_results: list[dict], cpu_threshold: float, ram_threshold: float) -> list[dict]:
    alerts = []
    cpu = metrics.get("cpu_percent", 0)
    ram = metrics.get("ram_percent", 0)

    if cpu >= cpu_threshold:
        alerts.append({
            "severity": "warning",
            "source": "system",
            "message": f"CPU usage is high ({cpu:.1f}%; threshold {cpu_threshold:.1f}%).",
        })
    if ram >= ram_threshold:
        alerts.append({
            "severity": "warning",
            "source": "system",
            "message": f"RAM usage is high ({ram:.1f}%; threshold {ram_threshold:.1f}%).",
        })
    for result in website_results:
        if result["status"] != "online":
            status = result.get("http_status")
            detail = f"HTTP {status}" if status is not None else result.get("error") or "no response"
            alerts.append({
                "severity": "critical" if result["status"] == "unreachable" else "warning",
                "source": "website",
                "url": result["url"],
                "message": f"Website check issue for {result['url']}: {detail}.",
            })
    return alerts
