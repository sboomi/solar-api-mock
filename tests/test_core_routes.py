import json

from solar_api_mock.core.main import get_building_insights, get_data_layers


def test_get_building_insights_default():
    response = get_building_insights({"lat": 0, "lon": 0})
    expected_response = {
        "name": "buildings/ChIJh0CMPQW7j4ARLrRiVvmg6Vs",
        "center": {"latitude": 37.4449739, "longitude": -122.13914659999998},
        "imageryDate": {"year": 2022, "month": 8, "day": 14},
        "postalCode": "94303",
        "administrativeArea": "CA",
        "statisticalArea": "06085511100",
        "regionCode": "US",
        "solarPotential": {
            "maxArrayPanelsCount": 987,
            "maxArrayAreaMeters2": 1938.0287,
            "maxSunshineHoursPerYear": 1811.3477,
            "carbonOffsetFactorKgPerMwh": 428.9201,
            "wholeRoofStats": {
                "areaMeters2": 2399.3958,
                "sunshineQuantiles": [
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
                "groundAreaMeters2": 2279.71,
            },
            "roofSegmentStats": [
                {
                    "pitchDegrees": 11.350553,
                    "azimuthDegrees": 269.6291,
                    "stats": {
                        "areaMeters2": 452.00052,
                        "sunshineQuantiles": [
                            409.601,
                            1482.1255,
                            1553.5117,
                            1582.7875,
                            1602.3456,
                            1613.7804,
                        ],
                        "groundAreaMeters2": 443.16,
                    },
                    "center": {
                        "latitude": 37.444972799999995,
                        "longitude": -122.13936369999999,
                    },
                    "boundingBox": {
                        "sw": {
                            "latitude": 37.444732099999996,
                            "longitude": -122.1394224,
                        },
                        "ne": {
                            "latitude": 37.4451909,
                            "longitude": -122.13929279999999,
                        },
                    },
                    "planeHeightAtCenterMeters": 10.7835045,
                },
                {
                    "pitchDegrees": 12.273684,
                    "azimuthDegrees": 179.12555,
                    "stats": {
                        "areaMeters2": 309.87268,
                        "sunshineQuantiles": [
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
                        "groundAreaMeters2": 302.79,
                    },
                    "center": {
                        "latitude": 37.4449286,
                        "longitude": -122.13898890000002,
                    },
                    "boundingBox": {
                        "sw": {"latitude": 37.4448617, "longitude": -122.1392095},
                        "ne": {
                            "latitude": 37.444981999999996,
                            "longitude": -122.1387809,
                        },
                    },
                    "planeHeightAtCenterMeters": 10.67585,
                },
            ],
            "solarPanelConfigs": [
                {
                    "panelsCount": 4,
                    "yearlyEnergyDcKwh": 2922.5322,
                    "roofSegmentSummaries": [
                        {
                            "pitchDegrees": 12.273684,
                            "azimuthDegrees": 179.12555,
                            "panelsCount": 4,
                            "yearlyEnergyDcKwh": 2922.532,
                            "segmentIndex": 1,
                        }
                    ],
                },
                {
                    "panelsCount": 5,
                    "yearlyEnergyDcKwh": 3651.4067,
                    "roofSegmentSummaries": [
                        {
                            "pitchDegrees": 12.273684,
                            "azimuthDegrees": 179.12555,
                            "panelsCount": 5,
                            "yearlyEnergyDcKwh": 3651.4065,
                            "segmentIndex": 1,
                        }
                    ],
                },
            ],
            "financialAnalyses": [
                {
                    "monthlyBill": {"currencyCode": "USD", "units": "20"},
                    "averageKwhPerMonth": -0.083333336,
                    "panelConfigIndex": -1,
                },
                {
                    "monthlyBill": {"currencyCode": "USD", "units": "25"},
                    "averageKwhPerMonth": -0.083333336,
                    "panelConfigIndex": -1,
                },
            ],
            "panelCapacityWatts": 400,
            "panelHeightMeters": 1.879,
            "panelWidthMeters": 1.045,
            "panelLifetimeYears": 20,
            "buildingStats": {
                "areaMeters2": 2533.6663,
                "sunshineQuantiles": [
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
                "groundAreaMeters2": 2356.03,
            },
            "solarPanels": [
                {
                    "center": {"latitude": 37.4449622, "longitude": -122.1390722},
                    "orientation": "LANDSCAPE",
                    "yearlyEnergyDcKwh": 731.7764,
                    "segmentIndex": 1,
                },
                {
                    "center": {
                        "latitude": 37.4449621,
                        "longitude": -122.13909340000001,
                    },
                    "orientation": "LANDSCAPE",
                    "yearlyEnergyDcKwh": 731.2524,
                    "segmentIndex": 1,
                },
            ],
        },
        "boundingBox": {
            "sw": {"latitude": 37.4447234, "longitude": -122.1394224},
            "ne": {"latitude": 37.4452242, "longitude": -122.13872160000001},
        },
        "imageryQuality": "HIGH",
        "imageryProcessedDate": {"year": 2024, "month": 10, "day": 15},
    }

    assert json.loads(response) == expected_response


def test_get_data_layers_default():
    response = get_data_layers({"lat": 0, "lon": 0}, 1000)
    expected_response = {
        "imageryDate": {"year": 2022, "month": 4, "day": 6},
        "imageryProcessedDate": {"year": 2023, "month": 8, "day": 4},
        "dsmUrl": "https://solar.googleapis.com/v1/geoTiff:get?id=ODU4ZmQ5NGUyNDA5ZDIxNzk1MjhkNzE0MmQ0Njk5M2QtOGVmZjdhMjQ4MzBiY2MxZDc1NDIxMzQ5OTAyZmUyNWY6RFNNOkxPVw",
        "rgbUrl": "https://solar.googleapis.com/v1/geoTiff:get?id=MzQwZjVlZDBhNDYxZWNhYjU2Y2NlOWQwMmVjNjVkMzEtZjBhMzgwMzA0YTNiMzZiMjNmZDQxOWI3OTA2YWVhNzM6UkdCOkxPVw",
        "maskUrl": "https://solar.googleapis.com/v1/geoTiff:get?id=NGQ5MTZmMTdhYTM3YTk3NTY1ZjMwZDcwZTExMWU1OWEtZDYxOTI0OTI1YzZlYjU5NDI5MjczY2QyMzQ3YWNlYTI6TUFTSzpMT1c",
        "annualFluxUrl": "https://solar.googleapis.com/v1/geoTiff:get?id=NWEyOGEwZjMwYjMxMzkyNmQzOTJkYmZjMjc4ZmJhYWYtYjVlMzc2ZjI0YmExYWZhYWQyNmVhNmVkNzFmODJkNjA6QU5OVUFMX0ZMVVg6TE9X",
        "monthlyFluxUrl": "https://solar.googleapis.com/v1/geoTiff:get?id=MjBlMTk1NTkxZGYwZTIxNjZjMWFjOWEzY2ZjZmVhMWEtYTRiZDIxOWUzMmQxYTUyNGE1NGMyYWYyZThlNTA4NTA6TU9OVEhMWV9GTFVYOkxPVw",
        "hourlyShadeUrls": [
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
        "imageryQuality": "HIGH",
    }

    assert json.loads(response) == expected_response
