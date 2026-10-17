
import time
import urllib.error
import urllib.request

from opspilot.logger_config import get_logger


logger = get_logger("OpsPilot.HealthChecker")


def check_website(url):
    """Check website availability, measure response time, and log results."""
    print(f"\nChecking: {url}")
    start_time = time.perf_counter()

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "OpsPilot/1.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            elapsed = (time.perf_counter() - start_time) * 1000
            result = (
                f"ONLINE (HTTP {response.status})"
                f" | Response: {elapsed:.2f} ms"
            )
            logger.info(
                "Website check succeeded | url=%s | status=%s | response_ms=%.2f",
                url,
                response.status,
                elapsed,
            )

    except urllib.error.HTTPError as error:
        elapsed = (time.perf_counter() - start_time) * 1000
        result = (
            f"SERVER RESPONDED (HTTP {error.code})"
            f" | Response: {elapsed:.2f} ms"
        )
        logger.warning(
            "Website returned HTTP error | url=%s | status=%s | response_ms=%.2f",
            url,
            error.code,
            elapsed,
        )

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        result = f"CHECK FAILED | {error}"
        logger.error("Website check failed | url=%s | error=%s", url, error)

    print(f"Result: {result}")
    return result
