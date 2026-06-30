from collections.abc import Sequence
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class PhotometricPoint(BaseModel):
    """
    Observed photometric point in an LSST alert report.
    Forced photometry (diaForcedSource) takes preference over alert photometry (diaSource.
    """

    time: Annotated[float, Field(description="midpointMjdTai")]
    flux: Annotated[float, Field(description="psfFlux")]
    fluxerr: Annotated[float, Field(description="psfFluxErr")]
    band: Annotated[str, Field(description="band")]
    zp: Annotated[float, Field(description="Photometric zero point")]
    zpsys: Annotated[str, Field(description="Zero point system")]


class Object(BaseModel):
    """Object associated with an LSST alert report (diaObject)"""

    id: Annotated[int, Field(description="diaObjectId")]
    external_id: Annotated[str | None, Field(description="External Object ID")] = None
    ra: Annotated[float, Field(description="Right ascension (ra; deg)")]
    ra_err: Annotated[float | None, Field(description="Right ascension uncertainty (raErr; deg)")] = None
    dec: Annotated[float, Field(description="Declination (dec; deg)")]
    dec_err: Annotated[float | None, Field(description="Declination uncertainty (decErr; deg)")] = None
    ra_dec_cov: Annotated[
        float | None, Field(description="Right ascension/declination covariance (ra_dec_Doc; deg2")
    ] = None
    source: Annotated[str, Field(description="Data source")]


class Host(BaseModel):
    """Host identified though catalog matching"""

    name: Annotated[str | None, Field(description="Name of the identifying ampel unit")]
    source: Annotated[str | list[str], Field(description="Names of the catalogs containing this host")]
    redshift: Annotated[
        float | None,
        Field(
            description=(
                "Mean of the best redshift category for all catalog sources containing redshifts (see "
                "https://github.com/AmpelAstro/Ampel-HU-astro/blob/main/ampel/contrib/hu/t2/T2DigestRedshifts.py"
            )
        ),
    ]
    redshift_error: Annotated[float | None, Field(description="Precision of the redshift category")] = None
    distance: float
    info: Annotated[
        str | dict[str, dict[str, str]] | None,
        Field(description="Type info if included in the matchjing catalogs, catalog name -> type key -> type value"),
    ] = None


class Feature(BaseModel):
    name: Annotated[str, Field(description="Feature name")]
    version: Annotated[str, Field(description="Feature version")]
    info: Annotated[str | None, Field(description="Description of the feature")]
    features: Annotated[dict[str, float], Field(description="Feature values")]


class MeanPosition(Feature):
    name: str = "mean_position"
    info: str = (
        "Mean position of the transient calculated from as "
        "the weighted sum of the diaSource positions contributing to the diaSource."
    )


class TemplateFlux(Feature):
    name: str = "template_flux"
    info: str = "Median of the templateFlux of all diaSources contributing to the diaObject."


class LSSTReport(BaseModel):
    """
    Data model for LSST alert reports from Ampel.
    """

    object: Object
    state: Annotated[
        int,
        Field(description="unique identifier for underlying collection of data points in AMPEL"),
    ]
    photometry: Sequence[PhotometricPoint]
    host: list[Host] = []
    classification: list = []
    features: list[MeanPosition | TemplateFlux] = []

    model_config = ConfigDict(extra="forbid")
