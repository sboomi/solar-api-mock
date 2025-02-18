from typing import Literal

from pydantic import BaseModel, Field


class SchemaProperties(BaseModel):
    pass


class FinancialDetailsProperties(SchemaProperties):
    """Details of a financial analysis.

    Some of these details are already stored at
    higher levels (e.g., out of pocket cost).
    Total money amounts are over a lifetime period
    defined by the panel_lifetime_years field
    in SolarPotential.

    Note: The out of pocket cost of purchasing the
    panels is given in the out_of_pocket_cost field
    in CashPurchaseSavings."""

    lifetimeSrecTotal: "MoneyProperties" = Field(
        description="Amount of money the user will receive from Solar Renewable Energy Credits over the panel lifetime; this applies if the user buys (with or without a loan) the panels.",
    )
    costOfElectricityWithoutSolar: "MoneyProperties" = Field(
        description="Total cost of electricity the user would have paid over the lifetime period if they didn't install solar.",
    )
    utilityIncentive: "MoneyProperties" = Field(
        description="Amount of money available from utility incentives; this applies if the user buys (with or without a loan) the panels.",
    )
    netMeteringAllowed: bool = Field(
        description="Whether net metering is allowed.",
    )
    stateIncentive: "MoneyProperties" = Field(
        description="Amount of money available from state incentives; this applies if the user buys (with or without a loan) the panels.",
    )
    percentageExportedToGrid: float = Field(
        description="The percentage (0-100) of solar electricity production we assumed was exported to the grid, based on the first quarter of production. This affects the calculations if net metering is not allowed.",
    )
    initialAcKwhPerYear: float = Field(
        description="How many AC kWh we think the solar panels will generate in their first year.",
    )
    remainingLifetimeUtilityBill: "MoneyProperties" = Field(
        description="Utility bill for electricity not produced by solar, for the lifetime of the panels.",
    )
    solarPercentage: float = Field(
        description="Percentage (0-100) of the user's power supplied by solar. Valid for the first year but approximately correct for future years.",
    )
    federalIncentive: "MoneyProperties" = Field(
        description="Amount of money available from federal incentives; this applies if the user buys (with or without a loan) the panels.",
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
    center: "LatLngProperties" = Field(
        description="A point near the center of the roof segment.",
    )
    azimuthDegrees: float = Field(
        description='Compass direction the roof segment is pointing in. 0 = North, 90 = East, 180 = South. For a "flat" roof segment (`pitch_degrees` very near 0), azimuth is not well defined, so for consistency, we define it arbitrarily to be 0 (North).',
    )
    planeHeightAtCenterMeters: float = Field(
        description="The height of the roof segment plane, in meters above sea level, at the point designated by `center`. Together with the pitch, azimuth, and center location, this fully defines the roof segment plane.",
    )
    boundingBox: "LatLngBoxProperties" = Field(
        description="The bounding box of the roof segment.",
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


class DataLayersProperties(SchemaProperties):
    """Information about the solar potential of a region.

    The actual data are contained in a number of GeoTIFF files
    covering the requested region, for which this message contains
    URLs: Each string in the `DataLayers` message contains a URL
    from which the corresponding GeoTIFF can be fetched.
    These URLs are valid for a few hours after they've been generated.
    Most of the GeoTIFF files are at a resolution of 0.1m/pixel,
    but the monthly flux file is at 0.5m/pixel, and the hourly
    shade files are at 1m/pixel. If a `pixel_size_meters` value
    was specified in the `GetDataLayersRequest`, then the
    minimum resolution in the GeoTIFF files will be that value.
    """

    annualFluxUrl: str = Field(
        description="The URL for the annual flux map (annual sunlight on roofs) of the region. Values are kWh/kW/year. This is *unmasked flux*: flux is computed for every location, not just building rooftops. Invalid locations are stored as -9999: locations outside our coverage area will be invalid, and a few locations inside the coverage area, where we were unable to calculate flux, will also be invalid.",
    )
    maskUrl: str = Field(
        description="The URL for the building mask image: one bit per pixel saying whether that pixel is considered to be part of a rooftop or not.",
    )
    imageryQuality: Literal[
        "IMAGERY_QUALITY_UNSPECIFIED", "HIGH", "MEDIUM", "LOW", "BASE"
    ] = Field(
        description="The quality of the result's imagery.",
    )
    monthlyFluxUrl: str = Field(
        description="The URL for the monthly flux map (sunlight on roofs, broken down by month) of the region. Values are kWh/kW/year. The GeoTIFF pointed to by this URL will contain twelve bands, corresponding to January...December, in order.",
    )
    imageryDate: "DateProperties" = Field(
        description="When the source imagery (from which all the other data are derived) in this region was taken. It is necessarily somewhat approximate, as the images may have been taken over more than one day.",
    )
    rgbUrl: str = Field(
        description="The URL for an image of RGB data (aerial photo) of the region.",
    )
    dsmUrl: str = Field(
        description="The URL for an image of the DSM (Digital Surface Model) of the region. Values are in meters above EGM96 geoid (i.e., sea level). Invalid locations (where we don't have data) are stored as -9999.",
    )
    hourlyShadeUrls: list[str] = Field(
        description='Twelve URLs for hourly shade, corresponding to January...December, in order. Each GeoTIFF will contain 24 bands, corresponding to the 24 hours of the day. Each pixel is a 32 bit integer, corresponding to the (up to) 31 days of that month; a 1 bit means that the corresponding location is able to see the sun at that day, of that hour, of that month. Invalid locations are stored as -9999 (since this is negative, it has bit 31 set, and no valid value could have bit 31 set as that would correspond to the 32nd day of the month). An example may be useful. If you want to know whether a point (at pixel location (x, y)) saw sun at 4pm on the 22nd of June you would: 1. fetch the sixth URL in this list (corresponding to June). 1. look up the 17th channel (corresponding to 4pm). 1. read the 32-bit value at (x, y). 1. read bit 21 of the value (corresponding to the 22nd of the month). 1. if that bit is a 1, then that spot saw the sun at 4pm 22 June. More formally: Given `month` (1-12), `day` (1...month max; February has 28 days) and `hour` (0-23), the shade/sun for that month/day/hour at a position `(x, y)` is the bit ``` (hourly_shade[month - 1])(x, y)[hour] & (1 << (day - 1)) ``` where `(x, y)` is spatial indexing, `[month - 1]` refers to fetching the `month - 1`st URL (indexing from zero), `[hour]` is indexing into the channels, and a final non-zero result means "sunny". There are no leap days, and DST doesn\'t exist (all days are 24 hours long; noon is always "standard time" noon).',
    )
    imageryProcessedDate: "DateProperties" = Field(
        description="When processing was completed on this imagery.", default=None
    )


class MoneyProperties(SchemaProperties):
    """Represents an amount of money with its currency type."""

    nanos: int = Field(
        description="""Number of nano (10^-9) units of the amount.
        The value must be between -999,999,999 and +999,999,999 inclusive.
        If `units` is positive, `nanos` must be positive or zero.
        If `units` is zero, `nanos` can be positive, zero, or negative.
        If `units` is negative, `nanos` must be negative or zero.
        For example $-1.75 is represented as `units`=-1 and `nanos`=-750,000,000.""",
        ge=-999_999_999,
        le=999_999_999,
        default=None,
    )
    units: str = Field(
        description='The whole units of the amount. For example if `currencyCode` is `"USD"`, then 1 unit is one US dollar.',
    )
    currencyCode: str = Field(
        description="The three-letter currency code defined in ISO 4217.",
    )


class LeasingSavingsProperties(SchemaProperties):
    """Cost and benefit of leasing a particular configuration of solar panels with a particular electricity usage."""

    savings: "SavingsOverTimeProperties" = Field(
        description="How much is saved (or not) over the lifetime period.",
    )
    leasesSupported: bool = Field(
        description="Whether leases are supported in this juristiction by the financial calculation engine. If this field is false, then the values in this message should probably be ignored. This is independent of `leases_allowed`: in some areas leases are allowed, but under conditions that aren't handled by the financial models.",
    )
    annualLeasingCost: "MoneyProperties" = Field(
        description="Estimated annual leasing cost.",
    )
    leasesAllowed: bool = Field(
        description="Whether leases are allowed in this juristiction (leases are not allowed in some states). If this field is false, then the values in this message should probably be ignored.",
    )


class CashPurchaseSavingsProperties(SchemaProperties):
    """Cost and benefit of an outright purchase of a
    particular configuration of solar panels with a
    particular electricity usage."""

    rebateValue: "MoneyProperties" = Field(
        description="The value of all tax rebates.",
    )
    savings: "SavingsOverTimeProperties" = Field(
        description="How much is saved (or not) over the lifetime period.",
    )
    upfrontCost: "MoneyProperties" = Field(
        description="Initial cost after tax incentives: it's the amount that must be paid during first year. Contrast with `out_of_pocket_cost`, which is before tax incentives.",
    )
    outOfPocketCost: "MoneyProperties" = Field(
        description="Initial cost before tax incentives: the amount that must be paid out-of-pocket. Contrast with `upfront_cost`, which is after tax incentives.",
    )
    paybackYears: float = Field(
        description="Number of years until payback occurs. A negative value means payback never occurs within the lifetime period.",
    )


class SavingsOverTimeProperties(SchemaProperties):
    """Financial information that's shared between different
    financing methods."""

    presentValueOfSavingsLifetime: "MoneyProperties" = Field(
        description="Using the assumed discount rate, what is the present value of the cumulative lifetime savings?",
    )
    presentValueOfSavingsYear20: "MoneyProperties" = Field(
        description="Using the assumed discount rate, what is the present value of the cumulative 20-year savings?",
    )
    savingsYear20: "MoneyProperties" = Field(
        description="Savings in the first twenty years after panel installation.",
    )
    financiallyViable: bool = Field(
        description="Indicates whether this scenario is financially viable. Will be false for scenarios with poor financial viability (e.g., money-losing).",
    )
    savingsLifetime: "MoneyProperties" = Field(
        description="Savings in the entire panel lifetime.",
    )
    savingsYear1: "MoneyProperties" = Field(
        description="Savings in the first year after panel installation.",
    )


class HttpBodyProperties(SchemaProperties):
    """Message that represents an arbitrary HTTP body. It should only be used for payload formats that can't be represented as JSON, such as raw binary or an HTML page. This message can be used both in streaming and non-streaming API methods in the request as well as the response. It can be used as a top-level request field, which is convenient if one wants to extract parameters from either the URL or HTTP template into the request fields and also want access to the raw HTTP body. Example: message GetResourceRequest { // A unique request id. string request_id = 1; // The raw HTTP body is bound to this field. google.api.HttpBody http_body = 2; } service ResourceService { rpc GetResource(GetResourceRequest) returns (google.api.HttpBody); rpc UpdateResource(google.api.HttpBody) returns (google.protobuf.Empty); } Example with streaming methods: service CaldavService { rpc GetCalendar(stream google.api.HttpBody) returns (stream google.api.HttpBody); rpc UpdateCalendar(stream google.api.HttpBody) returns (stream google.api.HttpBody); } Use of this type only changes how the request and response bodies are handled, all other features will continue to work unchanged."""

    data: str = Field(
        description="The HTTP request/response body as raw binary.",
        backref=None,
        format="byte",
        items="None",
        enum="None",
    )
    extensions: dict[str, str] = Field(
        description="Application specific response metadata. Must be set in the first response for streaming APIs.",
        backref=None,
        format="None",
        items="{'type': 'object', 'additionalProperties': {'type': 'any', 'description': 'Properties of the object. Contains field @type with type URL.'}}",
        enum="None",
    )
    contentType: str = Field(
        description="The HTTP Content-Type header value specifying the content type of the body.",
        backref=None,
        format="None",
        items="None",
        enum="None",
    )


class BuildingInsightsProperties(SchemaProperties):
    """Response message for `Solar.FindClosestBuildingInsights`.
    Information about the location, dimensions, and solar potential
    of a building."""

    administrativeArea: str = Field(
        description='Administrative area 1 (e.g., in the US, the state) that contains this building. For example, in the US, the abbreviation might be "MA" or "CA."',
    )
    imageryProcessedDate: "DateProperties" = Field(
        description="When processing was completed on this imagery.", default=None
    )
    center: "LatLngProperties" = Field(
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
    solarPotential: "SolarPotentialProperties" = Field(
        description="Solar potential of the building.",
    )
    regionCode: str = Field(
        description="Region code for the country (or region) this building is in.",
    )
    postalCode: str = Field(
        description="Postal code (e.g., US zip code) this building is contained by.",
    )
    imageryDate: "DateProperties" = Field(
        description="Date that the underlying imagery was acquired. This is approximate.",
    )
    statisticalArea: str = Field(
        description="Statistical area (e.g., US census tract) this building is in.",
    )
    boundingBox: "LatLngBoxProperties" = Field(
        description="The bounding box of the building.",
    )


class FinancedPurchaseSavingsProperties(SchemaProperties):
    """Cost and benefit of using a loan to buy a
    particular configuration of solar panels with a
    particular electricity usage."""

    annualLoanPayment: MoneyProperties = Field(
        description="Annual loan payments.",
    )
    rebateValue: MoneyProperties = Field(
        description="The value of all tax rebates (including Federal Investment Tax Credit (ITC)).",
    )
    savings: SavingsOverTimeProperties = Field(
        description="How much is saved (or not) over the lifetime period.",
    )
    loanInterestRate: float = Field(
        description="The interest rate on loans assumed in this set of calculations.",
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
    wholeRoofStats: "SizeAndSunshineStatsProperties" = Field(
        description="Total size and sunlight quantiles for the part of the roof that was assigned to some roof segment. Despite the name, this may not include the entire building. See building_stats.",
    )
    solarPanelConfigs: list["SolarPanelConfigProperties"] = Field(
        description="Each SolarPanelConfig describes a different arrangement of solar panels on the roof. They are in order of increasing number of panels. The `SolarPanelConfig` with panels_count=N is based on the first N panels in the `solar_panels` list. This field is only populated if at least 4 panels can fit on a roof.",
    )
    financialAnalyses: list["FinancialAnalysisProperties"] = Field(
        description="A FinancialAnalysis gives the savings from going solar assuming a given monthly bill and a given electricity provider. They are in order of increasing order of monthly bill amount. This field will be empty for buildings in areas for which the Solar API does not have enough information to perform financial computations.",
    )
    panelLifetimeYears: int = Field(
        description="The expected lifetime, in years, of the solar panels. This is used in the financial calculations.",
    )
    buildingStats: "SizeAndSunshineStatsProperties" = Field(
        description="Size and sunlight quantiles for the entire building, including parts of the roof that were not assigned to some roof segment. Because the orientations of these parts are not well characterised, the roof area estimate is unreliable, but the ground area estimate is reliable. It may be that a more reliable whole building roof area can be obtained by scaling the roof area from whole_roof_stats by the ratio of the ground areas of `building_stats` and `whole_roof_stats`.",
        default=None,
    )
    carbonOffsetFactorKgPerMwh: float = Field(
        description="Equivalent amount of CO2 produced per MWh of grid electricity. This is a measure of the carbon intensity of grid electricity displaced by solar electricity.",
    )
    roofSegmentStats: list["RoofSegmentSizeAndSunshineStatsProperties"] = Field(
        description="Size and sunlight quantiles for each roof segment.",
    )
    panelCapacityWatts: float = Field(
        description="Capacity, in watts, of the panel used in the calculations.",
    )
    solarPanels: list["SolarPanelProperties"] = Field(
        description="Each SolarPanel describes a single solar panel. They are listed in the order that the panel layout algorithm placed this. This is usually, though not always, in decreasing order of annual energy production.",
        default=None,
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


class DateProperties(SchemaProperties):
    """Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar.
    This can represent one of the following: * A full date, with non-zero year, month, and day values.
    * A month and day, with a zero year (for example, an anniversary).
    * A year on its own, with a zero month and a zero day.
    * A year and month, with a zero day (for example, a credit card expiration date).
    Related types: * google.type.TimeOfDay * google.type.DateTime * google.protobuf.Timestamp
    """

    month: int = Field(
        description="Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day.",
        backref=None,
        format="int32",
        items="None",
        enum="None",
    )
    day: int = Field(
        description="Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.",
        backref=None,
        format="int32",
        items="None",
        enum="None",
    )
    year: int = Field(
        description="Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.",
        backref=None,
        format="int32",
        items="None",
        enum="None",
    )


class FinancialAnalysisProperties(SchemaProperties):
    """Analysis of the cost and benefits of the optimum solar
    layout for a particular electric bill size."""

    defaultBill: bool = Field(
        description="Whether this is the bill size selected to be the default bill for the area this building is in. Exactly one `FinancialAnalysis` in `BuildingSolarPotential` should have `default_bill` set.",
        default=None,
    )
    panelConfigIndex: int = Field(
        description="Index in solar_panel_configs of the optimum solar layout for this bill size. This can be -1 indicating that there is no layout. In this case, the remaining submessages will be omitted.",
    )
    financialDetails: FinancialDetailsProperties = Field(
        description="Financial information that applies regardless of the financing method used.",
        default=None,
    )
    cashPurchaseSavings: CashPurchaseSavingsProperties = Field(
        description="Cost and benefit of buying the solar panels with cash.",
        default=None,
    )
    monthlyBill: MoneyProperties = Field(
        description="The monthly electric bill this analysis assumes.",
    )
    averageKwhPerMonth: float = Field(
        description="How much electricity the house uses in an average month, based on the bill size and the local electricity rates.",
    )
    leasingSavings: LeasingSavingsProperties = Field(
        description="Cost and benefit of leasing the solar panels.", default=None
    )
    financedPurchaseSavings: FinancedPurchaseSavingsProperties = Field(
        description="Cost and benefit of buying the solar panels by financing the purchase.",
        default=None,
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


class LatLngProperties(SchemaProperties):
    """An object that represents a latitude/longitude pair.

    This is expressed as a pair of doubles to represent
    degrees latitude and degrees longitude. Unless specified
    otherwise, this object must conform to the WGS84 standard.

    Values must be within normalized ranges."""

    longitude: float = Field(
        description="The longitude in degrees. It must be in the range [-180.0, +180.0].",
    )
    latitude: float = Field(
        description="The latitude in degrees. It must be in the range [-90.0, +90.0].",
    )


class LatLngBoxProperties(SchemaProperties):
    """A bounding box in lat/lng coordinates."""

    ne: LatLngProperties = Field(
        description="The northeast corner of the box.",
    )
    sw: LatLngProperties = Field(
        description="The southwest corner of the box.",
    )
