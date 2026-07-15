"""Kafka alert rate monitoring for Prometheus."""

import logging
from collections import deque
from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from statistics import median
from threading import Lock
from typing import Any

from prometheus_client import Counter, Gauge, start_http_server

from tdemocracy.listen import listen_to_nuclear_stream
from tdemocracy.model import NuclearTransientReport
from tdemocracy.settings import Settings

LOGGER = logging.getLogger(__name__)

# Prometheus metrics
alerts_count = Counter("nuclear_alerts_total", "Total nuclear alert reports received")
alerts_rate_per_hour = Gauge("nuclear_alerts_rate_per_hour", "Number of alerts in the last hour")
photometry_median_flux = Gauge(
    "nuclear_photometry_median_flux_latest", "Median flux of latest photometry point per hour"
)


class KafkaMetricsMonitor:
    """Monitor Kafka alert stream and track metrics."""

    def __init__(self, settings: Settings | None = None, metrics_port: int = 8000):
        """
        Initialize monitor.

        :param settings: Settings to use for stream connection
        :param metrics_port: Port for Prometheus metrics endpoint
        """
        self._settings = settings or Settings()
        self._metrics_port = metrics_port
        # ponytail: rolling window of (timestamp, flux) tuples, 1-hour retention
        self._hourly_window: deque[tuple[datetime, list[float]]] = deque()
        self._lock = Lock()

    def start_metrics_server(self) -> None:
        """Start Prometheus HTTP server."""
        LOGGER.info(f"Starting metrics server on port {self._metrics_port}")
        start_http_server(self._metrics_port)

    def process_alert(self, alert: NuclearTransientReport) -> None:
        """Process single alert and update metrics."""
        alerts_count.inc()

        if alert.photometry:
            latest_photometry = alert.photometry[-1]
            flux = latest_photometry.flux

            with self._lock:
                now = datetime.now(UTC)
                self._hourly_window.append((now, [flux]))

                cutoff = now - timedelta(hours=1)
                while self._hourly_window and self._hourly_window[0][0] < cutoff:
                    self._hourly_window.popleft()

                if self._hourly_window:
                    all_fluxes = [f for _, fluxes in self._hourly_window for f in fluxes]
                    alerts_rate_per_hour.set(len(self._hourly_window))
                    if all_fluxes:
                        photometry_median_flux.set(median(all_fluxes))

    def run_monitor(
        self,
        start_at: Any = None,
        until_eos: bool = False,
        skip_other_versions: bool = False,
    ) -> None:
        """
        Run monitoring loop (blocks until stream ends).

        :param start_at: Stream start position (from hop.io.StartPosition)
        :param until_eos: Stop at end-of-stream
        :param skip_other_versions: Skip mismatched model versions
        """
        self.start_metrics_server()

        stream: Generator[NuclearTransientReport] = listen_to_nuclear_stream(
            start_at=start_at,
            until_eos=until_eos,
            settings=self._settings,
            skip_other_versions=skip_other_versions,
        )

        LOGGER.info("Monitor starting...")
        for alert in stream:
            self.process_alert(alert)
            LOGGER.debug(f"Processed alert {alert.object.id}")


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO)
    monitor = KafkaMetricsMonitor()
    try:
        monitor.run_monitor()
    except KeyboardInterrupt:
        print("\nShutdown...")
        sys.exit(0)
