from typing import Literal

from pydantic import Field

from solar_api_mock.core.properties.base import SchemaProperties
from solar_api_mock.core.properties.common import LatLngBoxProperties, LatLngProperties
from solar_api_mock.core.properties.financial_analysis import (
    FinancialAnalysisProperties,
)


class SizeAndSunshineStatsProperties(SchemaProperties):
    """Size and sunniness quantiles of a roof, or part of a roof."""

    areaMeters2: float = Field(
        description="The area of the roof or roof segment, in m^2. This is the roof area (accounting for tilt), not the ground footprint area.",
    )
    sunshineQuantiles: list[float] = Field(
        description="Quantiles of the pointwise sunniness across the area. If there are N values here, this represents the (N-1)-iles. For example, if there are 5 values, then they would be the quartiles (min, 25%, 50%, 75%, max). Values are in annual kWh/kW like max_sunshine_hours_per_year.",
    )
    groundAreaMeters2: float = Field(
        description="The ground footprint area covered by the roof or roof segment, in m^2.",
    )


class RoofSegmentSummaryProperties(SchemaProperties):
    """Information about a roof segment on the
    building, with some number of panels placed on it."""

    yearlyEnergyDcKwh: float = Field(
        description="How much sunlight energy this part of the layout captures over the course of a year, in DC kWh, assuming the panels described above.",
    )
    segmentIndex: int = Field(
        description="Index in roof_segment_stats of the corresponding `RoofSegmentSizeAndSunshineStats`.",
    )
    panelsCount: int = Field(
        description="The total number of panels on this segment.",
    )
    azimuthDegrees: float = Field(
        description='Compass direction the roof segment is pointing in. 0 = North, 90 = East, 180 = South. For a "flat" roof segment (`pitch_degrees` very near 0), azimuth is not well defined, so for consistency, we define it arbitrarily to be 0 (North).',
    )
    pitchDegrees: float = Field(
        description="Angle of the roof segment relative to the theoretical ground plane. 0 = parallel to the ground, 90 = perpendicular to the ground.",
    )


class RoofSegmentSizeAndSunshineStatsProperties(SchemaProperties):
    """Information about the size and sunniness quantiles of a roof
    segment."""

    pitchDegrees: float = Field(
        description="Angle of the roof segment relative to the theoretical ground plane. 0 = parallel to the ground, 90 = perpendicular to the ground.",
    )
    stats: "SizeAndSunshineStatsProperties" = Field(
        description="Total size and sunlight quantiles for the roof segment.",
    )
    center: LatLngProperties = Field(
        description="A point near the center of the roof segment.",
    )
    azimuthDegrees: float = Field(
        description='Compass direction the roof segment is pointing in. 0 = North, 90 = East, 180 = South. For a "flat" roof segment (`pitch_degrees` very near 0), azimuth is not well defined, so for consistency, we define it arbitrarily to be 0 (North).',
    )
    planeHeightAtCenterMeters: float = Field(
        description="The height of the roof segment plane, in meters above sea level, at the point designated by `center`. Together with the pitch, azimuth, and center location, this fully defines the roof segment plane.",
    )
    boundingBox: LatLngBoxProperties = Field(
        description="The bounding box of the roof segment.",
    )


class SolarPanelProperties(SchemaProperties):
    """SolarPanel describes the position, orientation, and
    production of a single solar panel.

    See the panel_height_meters, panel_width_meters,
    and panel_capacity_watts fields in SolarPotential
    for information on the parameters of the panel."""

    orientation: Literal[
        "SOLAR_PANEL_ORIENTATION_UNSPECIFIED", "LANDSCAPE", "PORTRAIT"
    ] = Field(
        description="The orientation of the panel.",
    )
    yearlyEnergyDcKwh: float = Field(
        description="How much sunlight energy this layout captures over the course of a year, in DC kWh.",
    )
    segmentIndex: int = Field(
        description="Index in roof_segment_stats of the `RoofSegmentSizeAndSunshineStats` which corresponds to the roof segment that this panel is placed on.",
    )
    center: "LatLngProperties" = Field(
        description="The centre of the panel.",
    )


class SolarPanelConfigProperties(SchemaProperties):
    """SolarPanelConfig describes a particular placement
    of solar panels on the roof."""

    roofSegmentSummaries: list[RoofSegmentSummaryProperties] = Field(
        description="Information about the production of each roof segment that is carrying at least one panel in this layout. `roof_segment_summaries[i]` describes the i-th roof segment, including its size, expected production and orientation.",
    )
    panelsCount: int = Field(
        description="Total number of panels. Note that this is redundant to (the sum of) the corresponding fields in roof_segment_summaries.",
    )
    yearlyEnergyDcKwh: float = Field(
        description="How much sunlight energy this layout captures over the course of a year, in DC kWh, assuming the panels described above.",
    )


class SolarPotentialProperties(SchemaProperties):
    """Information about the solar potential of a building.
    A number of fields in this are defined in terms of "panels".
    The fields panel_capacity_watts, panel_height_meters,
    and panel_width_meters describe the parameters of
    the model of panel used in these calculations."""

    maxSunshineHoursPerYear: float = Field(
        description="Maximum number of sunshine hours received per year, by any point on the roof. Sunshine hours are a measure of the total amount of insolation (energy) received per year. 1 sunshine hour = 1 kWh per kW (where kW refers to kW of capacity under Standard Testing Conditions).",
    )
    maxArrayPanelsCount: int = Field(
        description="Size of the maximum array - that is, the maximum number of panels that can fit on the roof.",
    )
    panelHeightMeters: float = Field(
        description="Height, in meters in portrait orientation, of the panel used in the calculations.",
    )
    maxArrayAreaMeters2: float = Field(
        description="Size, in square meters, of the maximum array.",
    )
    panelWidthMeters: float = Field(
        description="Width, in meters in portrait orientation, of the panel used in the calculations.",
    )
    wholeRoofStats: SizeAndSunshineStatsProperties = Field(
        description="Total size and sunlight quantiles for the part of the roof that was assigned to some roof segment. Despite the name, this may not include the entire building. See building_stats.",
    )
    solarPanelConfigs: list[SolarPanelConfigProperties] = Field(
        description="Each SolarPanelConfig describes a different arrangement of solar panels on the roof. They are in order of increasing number of panels. The `SolarPanelConfig` with panels_count=N is based on the first N panels in the `solar_panels` list. This field is only populated if at least 4 panels can fit on a roof.",
    )
    financialAnalyses: list[FinancialAnalysisProperties] = Field(
        description="A FinancialAnalysis gives the savings from going solar assuming a given monthly bill and a given electricity provider. They are in order of increasing order of monthly bill amount. This field will be empty for buildings in areas for which the Solar API does not have enough information to perform financial computations.",
    )
    panelLifetimeYears: int = Field(
        description="The expected lifetime, in years, of the solar panels. This is used in the financial calculations.",
    )
    buildingStats: SizeAndSunshineStatsProperties = Field(
        description="Size and sunlight quantiles for the entire building, including parts of the roof that were not assigned to some roof segment. Because the orientations of these parts are not well characterised, the roof area estimate is unreliable, but the ground area estimate is reliable. It may be that a more reliable whole building roof area can be obtained by scaling the roof area from whole_roof_stats by the ratio of the ground areas of `building_stats` and `whole_roof_stats`.",
        default=None,
    )
    carbonOffsetFactorKgPerMwh: float = Field(
        description="Equivalent amount of CO2 produced per MWh of grid electricity. This is a measure of the carbon intensity of grid electricity displaced by solar electricity.",
    )
    roofSegmentStats: list[RoofSegmentSizeAndSunshineStatsProperties] = Field(
        description="Size and sunlight quantiles for each roof segment.",
    )
    panelCapacityWatts: float = Field(
        description="Capacity, in watts, of the panel used in the calculations.",
    )
    solarPanels: list[SolarPanelProperties] = Field(
        description="Each SolarPanel describes a single solar panel. They are listed in the order that the panel layout algorithm placed this. This is usually, though not always, in decreasing order of annual energy production.",
        default=None,
    )
