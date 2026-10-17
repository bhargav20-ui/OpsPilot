from datetime import datetime
import platform

import psutil


def get_system_metrics():
    """Collect basic system information and resource usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "computer": platform.node(),
        "operating_system": platform.system(),
        "cpu_usage": cpu_usage,
        "ram_usage": memory.percent,
        "available_ram_gb": round(memory.available / (1024 ** 3), 2),
    }


def display_system_metrics(metrics):
    """Display collected system metrics."""
    print("\n" + "=" * 45)
    print("             OpsPilot Monitor")
    print("=" * 45)
    print(f"Time: {metrics['timestamp']}")
    print(f"Operating System: {metrics['operating_system']}")
    print(f"Computer: {metrics['computer']}")
    print(f"CPU Usage: {metrics['cpu_usage']}%")
    print(f"RAM Usage: {metrics['ram_usage']}%")
    print(f"Available RAM: {metrics['available_ram_gb']:.2f} GB")