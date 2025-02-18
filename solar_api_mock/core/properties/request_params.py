from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator

from solar_api_mock.core.properties.common import LatLngProperties


class BuildingInsightsParams(BaseModel):
    lat_lon: LatLngProperties = Field(
        description="Required. The longitude and latitude from which the API looks for the nearest known building."
    )
    required_quality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = Field(
        default=None,
        description="Optional. The minimum quality level allowed in the results. No result with lower quality than this will be returned. Not specifying this is equivalent to restricting to HIGH quality only.",
    )

    @model_validator(mode="after")
    def fill_optional_values(self) -> Self:
        if self.required_quality is None:
            self.requiredQuality = "HIGH"

        return self


class DataLayersParams(BaseModel):
    """The parameters for the data layers API.

    Notes
    -----
    number: The limitations on this value are:
        * Any value up to 100m can always be specified.
        * Values over 100m can be specified, as long as
        radiusMeters <= pixelSizeMeters * 1000.
        * However, for values over 175m, the DataLayerView
        in the request must not include monthly flux or hourly shade.

    requiredQuality: No result with lower quality than this will be
    returned. Not specifying this is equivalent to restricting
    to HIGH quality only.

    pixelSizeMeters: Values of 0.1 (the default, if this
    field is not set explicitly), 0.25, 0.5, and 1.0
    are supported. Imagery components whose normal resolution
    is less than pixelSizeMeters will be returned at the
    resolution specified by pixelSizeMeters; imagery components
    whose normal resolution is equal to or greater than
    pixelSizeMeters will be returned at that normal resolution.

    exactQualityRequired: If set to false, the requiredQuality
    field is interpreted as the minimum required quality,
    such that HIGH quality imagery may be returned when
    requiredQuality is set to MEDIUM. If set to true,
    requiredQuality is interpreted as the exact required
    quality and only MEDIUM quality imagery is returned
    if requiredQuality is set to MEDIUM.

    """

    location: LatLngProperties = Field(
        description="Required. The longitude and latitude for the center of the region to get data for."
    )
    radius_meter: int = Field(
        description="Required. The radius, in meters, defining the region surrounding that centre point for which data should be returned."
    )
    view: Literal[
        "DATA_LAYER_VIEW_UNSPECIFIED",
        "DSM_LAYER",
        "IMAGERY_LAYERS",
        "IMAGERY_AND_ANNUAL_FLUX_LAYERS",
        "IMAGERY_AND_ALL_FLUX_LAYERS",
        "FULL_LAYERS",
    ] = Field(
        description="Optional. The desired subset of the data to return.", default=None
    )
    required_quality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = Field(
        description="Optional. The minimum quality level allowed in the results. No result with lower quality than this will be returned. Not specifying this is equivalent to restricting to HIGH quality only.",
        default=None,
    )
    pixel_size_numbers: float = Field(
        description="Optional. The minimum scale, in meters per pixel, of the data to return",
        default=None,
    )
    exact_quality_required: bool = Field(
        description="Optional. Whether to require exact quality of the imagery. ",
        default=None,
    )

    @model_validator(mode="after")
    def fill_optional_values(self) -> Self:
        if self.required_quality is None:
            self.required_quality = "HIGH"

        if self.pixel_size_meters is None:
            self.pixel_size_meters = 0.1

        if self.exact_quality_required is None:
            self.exact_quality_required = False

        return self
