from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict


class PhotometricPoint(BaseModel):
    """
    Observed photometric point in an LSST alert report.
    Forced photometry (diaForcedSource) takes preference over alert photometry (diaSource).
    """

    id: int
    """diaSourceId or diaForcedSourceId"""
    source: Literal["LSST_DP", "LSST_FP"]
    """id source"""
    time: float
    """midpointMjdTai"""
    flux: float
    """psfFlux"""
    fluxerr: float
    """psfFluxErr"""
    band: str
    """band"""
    zp: float
    """Photometric zero point"""
    zpsys: str
    """Zero point system"""


class Object(BaseModel):
    """Object associated with an LSST alert report (diaObject)"""

    id: int
    """diaObjectId"""
    external_id: str | None = None
    """External Object ID"""
    ra: float
    """Right ascension (ra; deg)"""
    ra_err: float | None = None
    """Right ascension uncertainty (raErr; deg)"""
    dec: float
    """Declination (dec; deg)"""
    dec_err: float | None = None
    """Declination uncertainty (decErr; deg)"""
    ra_dec_cov: float | None = None
    """Right ascension/declination covariance (ra_dec_Doc; deg2)"""
    source: str
    """Data source"""


class Host(BaseModel):
    """Host identified through catalog matching"""

    name: str | None
    """Name of the identifying ampel unit"""
    source: str | list[str]
    """Names of the catalogs containing this host"""
    redshift: float | None
    """Mean of the best redshift category for all catalog sources containing redshifts (see https://github.com/AmpelAstro/Ampel-HU-astro/blob/main/ampel/contrib/hu/t2/T2DigestRedshifts.py)"""
    redshift_error: float | None = None
    """Precision of the redshift category"""
    distance: float
    """Distance"""
    info: str | dict[str, dict[str, str]] | None = None
    """Type info if included in the matching catalogs, catalog name -> type key -> type value"""


class MeanPosition(BaseModel):
    """
    Mean position of the transient calculated as the
    weighted sum of the diaSource positions contributing to the diaSource.
    """

    mean_ra: float
    """The mean RA (deg)"""
    mean_dec: float
    """The mean Dec (deg)"""
    circularized_error: float
    """Geometric mean of sqrt(raErr^2 + decErr^2)"""
    std: float
    """Standard deviation of the datapoint distance to the mean position"""


template_flux_doc = """Median of the templateFlux of all diaSources contributing to the diaObject."""


class TemplateFlux(BaseModel):
    """Median and 90th percentile of the templateFlux of all diaSources
    contributing to the diaObject in a single band."""

    band: str
    """Band name"""
    median: float
    """Median template flux"""
    perc5: float
    """5th percentile template flux"""
    perc95: float
    """95th percentile template flux"""


class TemplateFluxes(BaseModel):
    """Median of the templateFlux of all diaSources contributing to the diaObject."""

    template_fluxes: dict[str, list[TemplateFlux]]
    """Mapping of band names to template fluxes."""


class NuclearTransientReport(BaseModel):
    """
    Data model for LSST alert reports from Ampel.
    """

    version: str
    """Version of the TDEmocracy nuclear filter"""
    object: Object
    state: int
    """unique identifier for underlying collection of data points in AMPEL"""
    photometry: Sequence[PhotometricPoint]
    host: list[Host] = []
    mean_position: MeanPosition
    template_fluxes: TemplateFluxes

    model_config = ConfigDict(extra="forbid")
