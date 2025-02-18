from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel

from solar_api_mock.core import properties, schema

app = FastAPI(prefix="/v1")


class BuildingInsightsParams(BaseModel):
    lat_lon: properties.LatLngProperties = properties.LatLngProperties(
        latitude=37.4449739, longitude=-122.139146599999980
    )
    required_quality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = None


class DataLayersParams(BaseModel):
    location: properties.LatLngProperties = properties.LatLngProperties(
        latitude=37.4449739, longitude=-122.139146599999980
    )
    radius_meter: int = 50
    view: Literal[
        "DATA_LAYER_VIEW_UNSPECIFIED",
        "DSM_LAYER",
        "IMAGERY_LAYERS",
        "IMAGERY_AND_ANNUAL_FLUX_LAYERS",
        "IMAGERY_AND_ALL_FLUX_LAYERS",
        "FULL_LAYERS",
    ] = None
    required_quality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = None
    pixel_size_numbers: float = None
    exact_quality_required: bool = None


async def get_building_insights_properties():
    builder = schema.BuildingInsightsBuilder()
    obj = builder.construct_model()
    return obj.properties


async def get_data_layers_properties():
    builder = schema.DataLayersBuilder()
    obj = builder.construct_model()
    return obj.properties


@app.get("/")
async def root():
    return {"message": "Welcome to Mock Solar API"}


@app.get(
    "/buildingInsights:findClosest",
    response_model=properties.BuildingInsightsProperties,
    response_model_exclude_none=True,
)
async def building_insights(
    building_insights_params_query: Annotated[BuildingInsightsParams, Query()],
):
    obj = await get_building_insights_properties()
    return obj


@app.get(
    "/dataLayers:get",
    response_model=properties.DataLayersProperties,
    response_model_exclude_none=True,
)
async def data_layers(data_layers_params_query: Annotated[DataLayersParams, Query()]):
    obj = await get_data_layers_properties()
    return obj
