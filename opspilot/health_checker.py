"""Website availability checks with explicit timeout and status classification."""
from __future__ import annotations

import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def check_website(url: str, timeout: float = 8.0, user_agent: str = "OpsPilot/1.0") -> dict:
    """Check a URL and return structured status, latency, and error information."""
    request = Request(url, headers={"User-Agent": user_agent}, method="GET")
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            latency_ms = round((time.perf_counter() - started) * 1000, 2)
            status_code = int(response.status)
            return {
                "url": url,
                "status": "online" if 200 <= status_code < 400 else "http_error",
                "http_status": status_code,
                "response_time_ms": latency_ms,
                "error": None,
            }
    except HTTPError as exc:
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "url": url,
            "status": "http_error",
            "http_status": int(exc.code),
            "response_time_ms": latency_ms,
            "error": str(exc.reason or exc),
        }
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        reason = getattr(exc, "reason", exc)
        return {
            "url": url,
            "status": "unreachable",
            "http_status": None,
            "response_time_ms": latency_ms,
            "error": str(reason),
        }
