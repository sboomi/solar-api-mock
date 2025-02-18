from pydantic import Field

from solar_api_mock.core.properties.base import SchemaProperties


class LatLngProperties(SchemaProperties):
    """An object that represents a latitude/longitude pair.

    This is expressed as a pair of doubles to represent
    degrees latitude and degrees longitude. Unless specified
    otherwise, this object must conform to the WGS84 standard.

    Values must be within normalized ranges."""

    longitude: float = Field(
        description="The longitude in degrees. It must be in the range [-180.0, +180.0].",
        le=180.0,
        ge=-180.0,
    )
    latitude: float = Field(
        description="The latitude in degrees. It must be in the range [-90.0, +90.0].",
        le=90.0,
        ge=-90.0,
    )


class LatLngBoxProperties(SchemaProperties):
    """A bounding box in lat/lng coordinates."""

    ne: LatLngProperties = Field(
        description="The northeast corner of the box.",
    )
    sw: LatLngProperties = Field(
        description="The southwest corner of the box.",
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
        ge=0,
        le=12,
    )
    day: int = Field(
        description="Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.",
        ge=0,
        le=31,
    )
    year: int = Field(
        description="Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.",
        ge=0,
        le=9999,
    )
