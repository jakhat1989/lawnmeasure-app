"""Houston metro aerial imagery source routing and source licensing guardrails."""
import unittest
from unittest.mock import Mock, patch
from imagery_registry import SOURCES,select_government_sources
from metro_imagery import metro_summary
from app import app

class HoustonImageryTests(unittest.TestCase):
 def test_public_galveston_2026_2025_one_inch_and_2024_three_inch(self):
  route=select_government_sources("TX",29.301,-94.797,"48167")
  self.assertEqual(route[:3],[
    "TX_GALVESTON_2026","TX_GALVESTON_2025_1IN","TX_GALVESTON_2024_3IN"])
  self.assertEqual(SOURCES["TX_GALVESTON_2025_1IN"][3],1)
  self.assertEqual(SOURCES["TX_GALVESTON_2024_3IN"][3],3)

 def test_houston_core_does_not_improperly_show_galveston_aerial(self):
  for coords in [(29.76,-95.37),(29.785,-95.821),(30.16,-95.46),
                 (29.62,-95.63)]:
   route=select_government_sources("TX",*coords,"48201")
   self.assertEqual(route[:2],["USGS_PLUS","USGS_NAIP"])
   self.assertTrue(all(not key.startswith("TX_GALVESTON") for key in route))

 def test_explicit_bounds_not_county_fips_controls_small_city_mosaic(self):
  # Areas of Galveston County well north of published city mosaic
  self.assertFalse(any(k.startswith("TX_GALVESTON") for k in
    select_government_sources("TX",29.68,-95.04,"48167")))

 def test_suburban_galveston_metro_loads_public_high_resolution(self):
  route=select_government_sources("TX",29.32,-94.78,"")
  self.assertEqual(route[0],"TX_GALVESTON_2026")

 def test_no_restricted_hgac_or_texas_hexagon_source_added(self):
  self.assertFalse(any("HGAC" in key or "HEXAGON" in key for key in SOURCES))

 def test_galveston_city_aerial_serves_with_public_provider_attribution(self):
  with app.test_client() as client:
   with client.session_transaction() as sess:sess["owner"]=True
   mock=Mock(content=bytes.fromhex("ffd8")+b"0"*7000,raise_for_status=Mock())
   with patch("app.http.get",return_value=mock) as request:
    response=client.get("/api/aerial",query_string={
      "lat":"29.301","lon":"-94.797","state":"TX","county_fips":"48167",
      "bbox":"-94.798,29.300,-94.796,29.302","width":"1200","height":"1200"})
    self.assertEqual(response.status_code,200)
    self.assertIn("Galveston",response.headers["X-Imagery-Source"])
    self.assertEqual(response.headers["X-Imagery-Provider"],"TX_GALVESTON_2026")
    self.assertIn("gis.galvestontx.gov",request.call_args.args[0])

 def test_houston_is_still_qa_pending(self):
  houston=metro_summary()["metros"][4]
  self.assertEqual(houston["rank"],5)
  self.assertFalse(houston["metro_image_qa_complete"])
  self.assertIn("H-GAC",houston["note"])

if __name__=="__main__":unittest.main()
