from typing import Type

from pydantic import BaseModel

from solar_api_mock.core import properties
from solar_api_mock.core.properties.base import SchemaProperties

schemas = {
    "FinancialDetails": """Details of a financial analysis. Some of these details are already stored at higher levels (e.g., out of pocket cost). Total money amounts are over a lifetime period defined by the panel_lifetime_years field in SolarPotential. Note: The out of pocket cost of purchasing the panels is given in the out_of_pocket_cost field in CashPurchaseSavings.""",
    "RoofSegmentSizeAndSunshineStats": """Information about the size and sunniness quantiles of a roof segment.""",
    "SizeAndSunshineStats": """Size and sunniness quantiles of a roof, or part of a roof.""",
    "DataLayers": """Information about the solar potential of a region. The actual data are contained in a number of GeoTIFF files covering the requested region, for which this message contains URLs: Each string in the `DataLayers` message contains a URL from which the corresponding GeoTIFF can be fetched. These URLs are valid for a few hours after they've been generated. Most of the GeoTIFF files are at a resolution of 0.1m/pixel, but the monthly flux file is at 0.5m/pixel, and the hourly shade files are at 1m/pixel. If a `pixel_size_meters` value was specified in the `GetDataLayersRequest`, then the minimum resolution in the GeoTIFF files will be that value.""",
    "Money": """Represents an amount of money with its currency type.""",
    "LeasingSavings": """Cost and benefit of leasing a particular configuration of solar panels with a particular electricity usage.""",
    "CashPurchaseSavings": """Cost and benefit of an outright purchase of a particular configuration of solar panels with a particular electricity usage.""",
    "SavingsOverTime": """Financial information that's shared between different financing methods.""",
    "HttpBody": """Message that represents an arbitrary HTTP body. It should only be used for payload formats that can't be represented as JSON, such as raw binary or an HTML page. This message can be used both in streaming and non-streaming API methods in the request as well as the response. It can be used as a top-level request field, which is convenient if one wants to extract parameters from either the URL or HTTP template into the request fields and also want access to the raw HTTP body. Example: message GetResourceRequest { // A unique request id. string request_id = 1; // The raw HTTP body is bound to this field. google.api.HttpBody http_body = 2; } service ResourceService { rpc GetResource(GetResourceRequest) returns (google.api.HttpBody); rpc UpdateResource(google.api.HttpBody) returns (google.protobuf.Empty); } Example with streaming methods: service CaldavService { rpc GetCalendar(stream google.api.HttpBody) returns (stream google.api.HttpBody); rpc UpdateCalendar(stream google.api.HttpBody) returns (stream google.api.HttpBody); } Use of this type only changes how the request and response bodies are handled, all other features will continue to work unchanged.""",
    "BuildingInsights": """Response message for `Solar.FindClosestBuildingInsights`. Information about the location, dimensions, and solar potential of a building.\"""",
    "FinancedPurchaseSavings": """Cost and benefit of using a loan to buy a particular configuration of solar panels with a particular electricity usage.""",
    "SolarPotential": """Information about the solar potential of a building. A number of fields in this are defined in terms of "panels". The fields panel_capacity_watts, panel_height_meters, and panel_width_meters describe the parameters of the model of panel used in these calculations.""",
    "SolarPanel": """SolarPanel describes the position, orientation, and production of a single solar panel. See the panel_height_meters, panel_width_meters, and panel_capacity_watts fields in SolarPotential for information on the parameters of the panel.""",
    "Date": """Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following: * A full date, with non-zero year, month, and day values. * A month and day, with a zero year (for example, an anniversary). * A year on its own, with a zero month and a zero day. * A year and month, with a zero day (for example, a credit card expiration date). Related types: * google.type.TimeOfDay * google.type.DateTime * google.protobuf.Timestamp""",
    "FinancialAnalysis": """Analysis of the cost and benefits of the optimum solar layout for a particular electric bill size.""",
    "RoofSegmentSummary": """Information about a roof segment on the building, with some number of panels placed on it.""",
    "SolarPanelConfig": """SolarPanelConfig describes a particular placement of solar panels on the roof.""",
    "LatLng": """An object that represents a latitude/longitude pair. This is expressed as a pair of doubles to represent degrees latitude and degrees longitude. Unless specified otherwise, this object must conform to the WGS84 standard. Values must be within normalized ranges.""",
    "LatLngBox": """A bounding box in lat/lng coordinates.""",
}


class SchemaModel(BaseModel):
    name: str
    description: str
    properties: SchemaProperties


class SchemaBuilder:
    def __init__(self, schema_name: str):
        if schema_name not in schemas:
            raise ValueError(f"Schema {schema_name} not found")
        self.schema_name = schema_name

    def construct_model(self):
        PropertiesModel = getattr(properties, f"{self.schema_name}Properties")

        properties_m = self._set_properties(PropertiesModel)

        return SchemaModel(
            name=self.schema_name,
            description=schemas[self.schema_name],
            properties=properties_m,
        )

    def _set_properties(self, model: Type[SchemaProperties]) -> SchemaProperties:
        pass


class BuildingInsightsBuilder(SchemaBuilder):
    def __init__(self, schema_name="BuildingInsights"):
        super().__init__(schema_name)

    def _set_properties(
        self, model: Type[properties.BuildingInsightsProperties]
    ) -> properties.BuildingInsightsProperties:
        return model(
            name="buildings/ChIJh0CMPQW7j4ARLrRiVvmg6Vs",
            center=properties.LatLngProperties(
                latitude=37.4449739, longitude=-122.13914659999998
            ),
            imageryDate=properties.DateProperties(year=2022, month=8, day=14),
            postalCode="94303",
            administrativeArea="CA",
            statisticalArea="06085511100",
            regionCode="US",
            solarPotential=properties.SolarPotentialProperties(
                buildingStats=properties.SizeAndSunshineStatsProperties(
                    areaMeters2=2533.6663,
                    groundAreaMeters2=2356.03,
                    sunshineQuantiles=[
                        348.80408,
                        1382.8478,
                        1467.4017,
                        1526.7751,
                        1557.0416,
                        1597.7374,
                        1626.1417,
                        1646.3545,
                        1669.879,
                        1764.1133,
                        1874.7046,
                    ],
                ),
                maxArrayPanelsCount=987,
                maxArrayAreaMeters2=1938.0287,
                maxSunshineHoursPerYear=1811.3477,
                carbonOffsetFactorKgPerMwh=428.9201,
                solarPanels=[
                    properties.SolarPanelProperties(
                        center=properties.LatLngProperties(
                            latitude=37.4449622, longitude=-122.1390722
                        ),
                        orientation="LANDSCAPE",
                        segmentIndex=1,
                        yearlyEnergyDcKwh=731.7764,
                    ),
                    properties.SolarPanelProperties(
                        center=properties.LatLngProperties(
                            latitude=37.4449621, longitude=-122.13909340000001
                        ),
                        orientation="LANDSCAPE",
                        segmentIndex=1,
                        yearlyEnergyDcKwh=731.2524,
                    ),
                ],
                wholeRoofStats=properties.SizeAndSunshineStatsProperties(
                    areaMeters2=2399.3958,
                    sunshineQuantiles=[
                        352.27243,
                        1402.5898,
                        1480.4432,
                        1534.5151,
                        1561.8411,
                        1603.2942,
                        1628.6796,
                        1647.9292,
                        1671.7146,
                        1767.0829,
                        1874.7046,
                    ],
                    groundAreaMeters2=2279.71,
                ),
                roofSegmentStats=[
                    properties.RoofSegmentSizeAndSunshineStatsProperties(
                        pitchDegrees=11.350553,
                        azimuthDegrees=269.6291,
                        stats=properties.SizeAndSunshineStatsProperties(
                            areaMeters2=452.00052,
                            sunshineQuantiles=[
                                409.601,
                                1482.1255,
                                1553.5117,
                                1582.7875,
                                1602.3456,
                                1613.7804,
                            ],
                            groundAreaMeters2=443.16,
                        ),
                        center=properties.LatLngProperties(
                            latitude=37.444972799999995, longitude=-122.13936369999999
                        ),
                        boundingBox=properties.LatLngBoxProperties(
                            imageryProcessedDate=properties.DateProperties(
                                day=15,
                                month=10,
                                year=2024,
                            ),
                            imageryQuality="HIGH",
                            sw=properties.LatLngProperties(
                                latitude=37.444732099999996, longitude=-122.1394224
                            ),
                            ne=properties.LatLngProperties(
                                latitude=37.4451909, longitude=-122.13929279999999
                            ),
                        ),
                        planeHeightAtCenterMeters=10.7835045,
                    ),
                    properties.RoofSegmentSizeAndSunshineStatsProperties(
                        pitchDegrees=12.273684,
                        azimuthDegrees=179.12555,
                        stats=properties.SizeAndSunshineStatsProperties(
                            areaMeters2=309.87268,
                            sunshineQuantiles=[
                                650.5504,
                                1701.709,
                                1745.0032,
                                1768.4081,
                                1779.1625,
                                1787.4258,
                                1794.9333,
                                1801.3938,
                                1806.7461,
                                1814.0724,
                                1845.8717,
                            ],
                            groundAreaMeters2=302.79,
                        ),
                        center=properties.LatLngProperties(
                            latitude=37.4449286, longitude=-122.13898890000002
                        ),
                        boundingBox=properties.LatLngBoxProperties(
                            sw=properties.LatLngProperties(
                                latitude=37.4448617, longitude=-122.1392095
                            ),
                            ne=properties.LatLngProperties(
                                latitude=37.444981999999996, longitude=-122.1387809
                            ),
                        ),
                        planeHeightAtCenterMeters=10.67585,
                    ),
                ],
                solarPanelConfigs=[
                    properties.SolarPanelConfigProperties(
                        panelsCount=4,
                        yearlyEnergyDcKwh=2922.5322,
                        roofSegmentSummaries=[
                            properties.RoofSegmentSummaryProperties(
                                pitchDegrees=12.273684,
                                azimuthDegrees=179.12555,
                                panelsCount=4,
                                yearlyEnergyDcKwh=2922.532,
                                segmentIndex=1,
                            )
                        ],
                    ),
                    properties.SolarPanelConfigProperties(
                        panelsCount=5,
                        yearlyEnergyDcKwh=3651.4067,
                        roofSegmentSummaries=[
                            properties.RoofSegmentSummaryProperties(
                                pitchDegrees=12.273684,
                                azimuthDegrees=179.12555,
                                panelsCount=5,
                                yearlyEnergyDcKwh=3651.4065,
                                segmentIndex=1,
                            )
                        ],
                    ),
                ],
                financialAnalyses=[
                    properties.FinancialAnalysisProperties(
                        monthlyBill=properties.MoneyProperties(
                            currencyCode="USD", units="20"
                        ),
                        averageKwhPerMonth=-0.083333336,
                        panelConfigIndex=-1,
                    ),
                    properties.FinancialAnalysisProperties(
                        monthlyBill=properties.MoneyProperties(
                            currencyCode="USD", units="25"
                        ),
                        averageKwhPerMonth=-0.083333336,
                        panelConfigIndex=-1,
                    ),
                ],
                panelCapacityWatts=400,
                panelHeightMeters=1.879,
                panelWidthMeters=1.045,
                panelLifetimeYears=20,
            ),
            boundingBox=properties.LatLngBoxProperties(
                sw=properties.LatLngProperties(
                    latitude=37.4447234, longitude=-122.1394224
                ),
                ne=properties.LatLngProperties(
                    latitude=37.4452242, longitude=-122.13872160000001
                ),
            ),
            imageryQuality="HIGH",
            imageryProcessedDate=properties.DateProperties(year=2024, month=10, day=15),
        )


class DataLayersBuilder(SchemaBuilder):
    def __init__(self, schema_name="DataLayers"):
        super().__init__(schema_name)

    def _set_properties(
        self, model: Type[properties.DataLayersProperties]
    ) -> properties.DataLayersProperties:
        return model(
            imageryDate=properties.DateProperties(year=2022, month=4, day=6),
            imageryProcessedDate=properties.DateProperties(year=2023, month=8, day=4),
            dsmUrl="https://solar.googleapis.com/v1/geoTiff:get?id=ODU4ZmQ5NGUyNDA5ZDIxNzk1MjhkNzE0MmQ0Njk5M2QtOGVmZjdhMjQ4MzBiY2MxZDc1NDIxMzQ5OTAyZmUyNWY6RFNNOkxPVw",
            rgbUrl="https://solar.googleapis.com/v1/geoTiff:get?id=MzQwZjVlZDBhNDYxZWNhYjU2Y2NlOWQwMmVjNjVkMzEtZjBhMzgwMzA0YTNiMzZiMjNmZDQxOWI3OTA2YWVhNzM6UkdCOkxPVw",
            maskUrl="https://solar.googleapis.com/v1/geoTiff:get?id=NGQ5MTZmMTdhYTM3YTk3NTY1ZjMwZDcwZTExMWU1OWEtZDYxOTI0OTI1YzZlYjU5NDI5MjczY2QyMzQ3YWNlYTI6TUFTSzpMT1c",
            annualFluxUrl="https://solar.googleapis.com/v1/geoTiff:get?id=NWEyOGEwZjMwYjMxMzkyNmQzOTJkYmZjMjc4ZmJhYWYtYjVlMzc2ZjI0YmExYWZhYWQyNmVhNmVkNzFmODJkNjA6QU5OVUFMX0ZMVVg6TE9X",
            monthlyFluxUrl="https://solar.googleapis.com/v1/geoTiff:get?id=MjBlMTk1NTkxZGYwZTIxNjZjMWFjOWEzY2ZjZmVhMWEtYTRiZDIxOWUzMmQxYTUyNGE1NGMyYWYyZThlNTA4NTA6TU9OVEhMWV9GTFVYOkxPVw",
            hourlyShadeUrls=[
                "https://solar.googleapis.com/v1/geoTiff:get?id=YWRhOGIwNDc5OTViNDI4ZWRhYWMzMGJkZDU5ZjYzZmItNmIzODc3ZWIzNmJiYTAzNjI4M2RlZDdkYzFkZTNjOTQ6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=MTE5MDg1Y2NlYThjMTJjMDIzOTc5ZTAxYzJiNTY1NWMtNjU3MDE2MWY5ZmZhMGQ5NzU3ZTJlNmE1NTBjNzE3MzE6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=M2I1MWY2YmY3ZjZjNzlhNTIwMjVmZDYwNTAxY2Q0ZGEtZDI5OWM5YzM1YWI4Y2U4ODE4YjFiOWJjNTNiNjQyNjA6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=NjcwMzQ2OGQ1OWFiMGFlZTc0MGQzMTQ1MDBhNmJiYWMtNTRhZDYwNmFlNzJjYzMzMTQxMmY1NDg3MDhkYzc2ZTA6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=ZTlkYTc3YzAzYWE1ZDBjMTE2OWI2YmZlZjEzODg0NTYtMTY5MmY2NmJhZjJlYzJlOTNiYmEzNjIxZjUxZDY3NGM6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=NjhlOWNlYjExMTY2YjVhODgwZTE4MWY4NWVjNGVhNjQtNTczODExYWMzM2M4NGRkZTE1OWE0ZDUxYWVhYTA3ZTU6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=YzM1ZGIxNTIwNGI5ZGNiM2M5YjIwNTQ3ODhiMjQ4YzMtZGViZGNlNThhZDI3ODIyYzAwMTIyYzdhOTkxNzRmYWM6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=MzE2OGRlMGRhNWZhMzcyMzI0NmE0MjVkM2JjZWU5M2ItZGQxNGZjOGFhNTgzYWE0ZDE2ZDU1ZGZhNTE2Yzg3YmM6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=ZDVkOThjMjFiZjMzNjRhYTM3YTk3OGUwNWE2MjhlZDctYjk3YTY2MGQ1ZGFjNzA3MTQ4ZWRiZTc1NjQ0YWQ3MjE6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=ODVkMDA5Mzg0OGQ4ODNhYjAyN2I3ZTEwYjk4MjI1ODQtMjdiNGNmZjk2MjQ4MDc4MzRkOWUzZTU5MzY1OThkOTM6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=MTA4YTQ1ZjEyZTMzZjU4Yzc5NzA5MTNjMzA0MzdhODItMmZiNmYxMjM5OWY4ZjY3OGUxMzg5MTY1Y2VkNmNlMDA6SE9VUkxZX1NIQURFOkxPVw",
                "https://solar.googleapis.com/v1/geoTiff:get?id=MDk3ZThlZjU3NjM4ZTFmMTIzZjNjYTFmNTY5ODViOGQtZDJhN2YzM2JjNzQxODE5YTgyZDk4ZTI0MDcxY2I0MDg6SE9VUkxZX1NIQURFOkxPVw",
            ],
            imageryQuality="HIGH",
        )
