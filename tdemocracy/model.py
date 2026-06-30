from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict


class PhotometricPoint(BaseModel):
    """
    Observed photometric point in an LSST alert report.
    Forced photometry (diaForcedSource) takes preference over alert photometry (diaSource.
    """

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


class Feature(BaseModel):
    name: str
    """Feature name"""
    version: str
    """Feature version"""
    info: str | None
    """Description of the feature"""
    features: dict[str, float]
    """Feature values"""


mean_position_doc = (
    "Mean position of the transient calculated from as the "
    "weighted sum of the diaSource positions contributing to the diaSource."
)


class MeanPosition(Feature):
    __doc__ = mean_position_doc
    name: str = "mean_position"
    info: str = mean_position_doc


template_flux_doc = """Median of the templateFlux of all diaSources contributing to the diaObject."""


class TemplateFlux(Feature):
    __doc__ = template_flux_doc
    name: str = "template_flux"
    info: str = template_flux_doc


class LSSTReport(BaseModel):
    """
    Data model for LSST alert reports from Ampel.
    """

    object: Object
    state: int
    """unique identifier for underlying collection of data points in AMPEL"""
    photometry: Sequence[PhotometricPoint]
    host: list[Host] = []
    classification: list = []
    features: list[MeanPosition | TemplateFlux] = []

    model_config = ConfigDict(extra="forbid")
