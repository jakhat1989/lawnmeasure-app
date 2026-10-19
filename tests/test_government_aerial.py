"""Government image service routing and fallback behavior (no external network)."""
import unittest
from unittest.mock import patch
from app import app, select_government_sources

class FakeImageResponse:
    content=b"\xff\xd8"+b"\x00"*6000
    headers={"Content-Type":"image/jpeg"}
    def raise_for_status(self):return None

class AerialRoutingTests(unittest.TestCase):
    def test_cook_county_uses_county_imagery_first(self):
        route=select_government_sources("IL",41.9784,-87.7995)
        self.assertEqual(route[0],"IL_COOK")
        self.assertEqual(route[-1],"USGS_NAIP")

    def test_ocala_uses_marion_county_imagery_first(self):
        route=select_government_sources("FL",29.2125,-82.1108)
        self.assertEqual(route[:2],["FL_MARION_2024","FL_MARION"])

    def test_unregistered_state_uses_national_fallback(self):
        self.assertEqual(select_government_sources("TX",31.9,-97.1),
                         ["USGS_PLUS","USGS_NAIP"])

    def test_image_endpoint_records_source(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["owner"]=True
            with patch("app.http.get",return_value=FakeImageResponse()) as get:
                resp=client.get("/api/aerial",query_string={
                    "lat":"41.9784","lon":"-87.7995","state":"IL",
                    "bbox":"-87.801,41.977,-87.798,41.980",
                    "width":"1200","height":"1200"})
                self.assertEqual(resp.status_code,200)
                self.assertIn("Cook County",resp.headers["X-Imagery-Source"])
                self.assertEqual(resp.headers["X-Imagery-Coverage"],"regional")
                self.assertIn("gis.cookcountyil.gov",get.call_args.args[0])

    def test_image_requires_login(self):
        with app.test_client() as client:
            response=client.get("/api/aerial")
            self.assertEqual(response.status_code,401)

if __name__=="__main__":unittest.main()
