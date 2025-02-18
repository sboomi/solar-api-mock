from typing import Literal

from solar_api_mock.core.properties import LatLngProperties
from solar_api_mock.core.schema import BuildingInsightsBuilder, DataLayersBuilder


def get_building_insights(
    lat_lon: LatLngProperties,
    required_quality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = None,
):
    builder = BuildingInsightsBuilder()
    obj = builder.construct_model()
    return obj.properties.model_dump_json(exclude_none=True)


def get_data_layers(
    location: LatLngProperties,
    radius_meter: int,
    view: Literal[
        "DATA_LAYER_VIEW_UNSPECIFIED",
        "DSM_LAYER",
        "IMAGERY_LAYERS",
        "IMAGERY_AND_ANNUAL_FLUX_LAYERS",
        "IMAGERY_AND_ALL_FLUX_LAYERS",
        "FULL_LAYERS",
    ] = None,
    required_quality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = None,
    pixel_size_numbers: float = None,
    exact_quality_required: bool = None,
):
    builder = DataLayersBuilder()
    obj = builder.construct_model()
    return obj.properties.model_dump_json(exclude_none=True)
