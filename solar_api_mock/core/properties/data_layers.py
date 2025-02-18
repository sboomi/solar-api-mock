from typing import Literal

from pydantic import Field

from solar_api_mock.core.properties.base import SchemaProperties
from solar_api_mock.core.properties.common import DateProperties


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
    imageryDate: DateProperties = Field(
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
    imageryProcessedDate: DateProperties = Field(
        description="When processing was completed on this imagery.", default=None
    )
