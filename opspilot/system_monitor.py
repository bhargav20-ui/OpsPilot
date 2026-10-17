"""Collect live system metrics."""
from __future__ import annotations

import platform
import socket
from datetime import datetime, timezone

import psutil


def get_system_metrics() -> dict:
    """Return a snapshot of current system utilization."""
    memory = psutil.virtual_memory()
    return {
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "operating_system": f"{platform.system()} {platform.release()}",
        "cpu_percent": round(psutil.cpu_percent(interval=0.2), 1),
        "ram_percent": round(memory.percent, 1),
        "available_ram_gb": round(memory.available / (1024 ** 3), 2),
        "total_ram_gb": round(memory.total / (1024 ** 3), 2),
    }
