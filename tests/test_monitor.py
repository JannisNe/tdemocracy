"""Tests for monitor module."""

from tdemocracy.model import MeanPosition, NuclearTransientReport, Object, PhotometricPoint, TemplateFluxes
from tdemocracy.monitor import KafkaMetricsMonitor, alerts_count, alerts_rate_per_hour, photometry_median_flux


def create_test_alert(flux: float = 100.0) -> NuclearTransientReport:
    """Create a minimal test alert."""
    return NuclearTransientReport(
        version="1.0",
        model_version="1.0",
        object=Object(id=1, ra=0.0, dec=0.0, source="test"),
        state=1,
        photometry=[
            PhotometricPoint(
                id=1, source="LSST_DP", time=60000.0, flux=flux, fluxerr=1.0, band="g", zp=30.0, zpsys="ab"
            )
        ],
        host=None,
        mean_position=MeanPosition(mean_ra=0.0, mean_dec=0.0, circularized_error=0.1, std=0.05),
        template_fluxes=TemplateFluxes(**dict.fromkeys("ugrizy")),
    )


def test_monitor_process_alert():
    """Test that alert processing updates metrics."""
    monitor = KafkaMetricsMonitor()
    initial_count = float(alerts_count._value.get())

    alert = create_test_alert(flux=50.0)
    monitor.process_alert(alert)

    assert float(alerts_count._value.get()) == initial_count + 1
    assert float(alerts_rate_per_hour._value.get()) == 1
    assert float(photometry_median_flux._value.get()) == 50.0


def test_monitor_multiple_alerts():
    """Test that multiple alerts update rate and median correctly."""
    monitor = KafkaMetricsMonitor()

    for flux in [100.0, 200.0, 150.0]:
        monitor.process_alert(create_test_alert(flux=flux))

    rate = float(alerts_rate_per_hour._value.get())
    median_flux = float(photometry_median_flux._value.get())

    assert rate == 3
    assert median_flux == 150.0  # median of [100, 200, 150]
