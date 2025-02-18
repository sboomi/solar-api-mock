from typing import Literal

from pydantic import Field

from solar_api_mock.core.properties.base import SchemaProperties
from solar_api_mock.core.properties.common import (
    DateProperties,
    LatLngBoxProperties,
    LatLngProperties,
)
from solar_api_mock.core.properties.solar_potential import SolarPotentialProperties


class BuildingInsightsProperties(SchemaProperties):
    """Response message for `Solar.FindClosestBuildingInsights`.
    Information about the location, dimensions, and solar potential
    of a building."""

    administrativeArea: str = Field(
        description='Administrative area 1 (e.g., in the US, the state) that contains this building. For example, in the US, the abbreviation might be "MA" or "CA."',
    )
    imageryProcessedDate: DateProperties = Field(
        description="When processing was completed on this imagery.", default=None
    )
    center: LatLngProperties = Field(
        description="A point near the center of the building.",
    )
    imageryQuality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = Field(
        description="The quality of the imagery used to compute the data for this building.",
        default=None,
    )
    name: str = Field(
        description="The resource name for the building, of the format `buildings/{place_id}`.",
    )
    solarPotential: SolarPotentialProperties = Field(
        description="Solar potential of the building.",
    )
    regionCode: str = Field(
        description="Region code for the country (or region) this building is in.",
    )
    postalCode: str = Field(
        description="Postal code (e.g., US zip code) this building is contained by.",
    )
    imageryDate: DateProperties = Field(
        description="Date that the underlying imagery was acquired. This is approximate.",
    )
    statisticalArea: str = Field(
        description="Statistical area (e.g., US census tract) this building is in.",
    )
    boundingBox: LatLngBoxProperties = Field(
        description="The bounding box of the building.",
    )
