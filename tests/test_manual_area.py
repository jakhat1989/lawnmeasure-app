"""Regression tests for manually drawn lawn measurements."""
import math
import os
import unittest

from app import app, measured


def rectangle(lon=-84.726, lat=39.072, width=0.0003, height=0.0002):
    return {
        "type": "Polygon",
        "coordinates": [[
            [lon, lat], [lon+width, lat],
            [lon+width, lat+height], [lon, lat+height], [lon, lat]
        ]]
    }


class AreaTests(unittest.TestCase):
    def test_empty_area_after_clear(self):
        self.assertEqual(measured({"areas": [], "exclusions": []}),
                         {"area_sqft": 0, "gross_sqft": 0, "excluded_sqft": 0})

    def test_lawn_rectangle_measures_positive_sqft(self):
        result = measured({"areas": [rectangle()], "exclusions": []})
        self.assertGreater(result["area_sqft"], 1000)
        self.assertEqual(result["area_sqft"], result["gross_sqft"])
        self.assertEqual(result["excluded_sqft"], 0)

    def test_house_exclusion_subtracts_area(self):
        lawn = rectangle()
        house = rectangle(lon=-84.72592, lat=39.07205, width=0.00012, height=0.00008)
        result = measured({"areas": [lawn], "exclusions": [house]})
        self.assertGreater(result["gross_sqft"], result["area_sqft"])
        self.assertGreater(result["excluded_sqft"], 0)
        self.assertAlmostEqual(result["area_sqft"]+result["excluded_sqft"],
                               result["gross_sqft"], delta=2)

    def test_overlapping_lawn_polygons_do_not_double_count(self):
        lawn = rectangle()
        same = measured({"areas": [lawn, lawn], "exclusions": []})
        single = measured({"areas": [lawn], "exclusions": []})
        self.assertEqual(same["area_sqft"], single["area_sqft"])

    def test_unrelated_exclusion_does_not_reduce_area(self):
        lawn = rectangle()
        outside = rectangle(lon=-84.71, lat=39.09)
        result = measured({"areas": [lawn], "exclusions": [outside]})
        self.assertEqual(result["area_sqft"], result["gross_sqft"])

    def test_api_requires_sign_in(self):
        with app.test_client() as client:
            response = client.post("/api/area", json={"areas":[rectangle()]})
            self.assertEqual(response.status_code, 401)

    def test_authenticated_api_returns_sqft_then_zero_when_cleared(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["owner"] = True
            measured_response = client.post("/api/area",
                json={"areas":[rectangle()], "exclusions":[]})
            self.assertEqual(measured_response.status_code, 200)
            self.assertGreater(measured_response.json["area_sqft"], 1000)
            cleared_response = client.post("/api/area",
                json={"areas":[], "exclusions":[]})
            self.assertEqual(cleared_response.status_code, 200)
            self.assertEqual(cleared_response.json["area_sqft"], 0)


if __name__ == "__main__":
    unittest.main()
