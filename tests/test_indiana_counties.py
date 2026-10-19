"""Indiana county routing and resolution claims - network-independent."""
import unittest
from unittest.mock import Mock, patch
from imagery_registry import SOURCES, select_government_sources, coverage_summary
from indiana_imagery import (
 INDIANA_COUNTIES,INDIANA_2026_3IN_DOWNLOAD_COUNTIES,
 INDIANA_2025_6IN_LEAF_ON_DOWNLOAD_COUNTIES,
 indiana_county_info, indiana_summary)
from app import app

class IndianaTests(unittest.TestCase):
 def test_92_official_indiana_counties_and_fips(self):
  self.assertEqual(len(INDIANA_COUNTIES),92)
  self.assertEqual(sorted(INDIANA_COUNTIES),[f"18{n:03d}" for n in range(1,184,2)])
  self.assertEqual(INDIANA_COUNTIES["18057"],"Hamilton")
  self.assertEqual(INDIANA_COUNTIES["18081"],"Johnson")
  self.assertEqual(INDIANA_COUNTIES["18183"],"Whitley")

 def test_hamilton_three_inch_stays_above_state_current(self):
  ids=select_government_sources("IN",40.06,-86.1,"18057")
  self.assertEqual(ids[:2],["IN_HAMILTON_2024_3IN","IN_CURRENT"])
  self.assertEqual(SOURCES[ids[0]][3],3)

 def test_johnson_north_partial_newer_source_first(self):
  ids=select_government_sources("IN",39.5,-86.09,"18081")
  self.assertEqual(ids[:2],["IN_JOHNSON_NORTH_2025","IN_CURRENT"])
  self.assertIsNone(SOURCES[ids[0]][3])

 def test_every_other_county_uses_IGIO_current(self):
  for fips in INDIANA_COUNTIES:
   row=indiana_county_info(fips)
   self.assertFalse(row["county_completed"])
   source_ids=select_government_sources("IN",39.2,-86.4,fips)
   self.assertIn("IN_CURRENT",source_ids)
   self.assertEqual(source_ids[-2:],["USGS_PLUS","USGS_NAIP"])

 def test_nine_2026_three_inch_bulk_downloads_not_misrepresented(self):
  self.assertEqual(len(INDIANA_2026_3IN_DOWNLOAD_COUNTIES),9)
  self.assertIn("Monroe",INDIANA_2026_3IN_DOWNLOAD_COUNTIES)
  self.assertIn("Bartholomew",INDIANA_2026_3IN_DOWNLOAD_COUNTIES)
  m=indiana_county_info("18105")
  self.assertTrue(m["has_2026_three_inch_bulk_release"])
  self.assertEqual(m["preferred_streaming_source"],"IN_CURRENT")
  self.assertFalse(m["county_completed"])

 def test_2025_leaf_on_download_release_separate(self):
  self.assertEqual(len(INDIANA_2025_6IN_LEAF_ON_DOWNLOAD_COUNTIES),11)
  self.assertTrue(indiana_county_info("18089")["has_2025_six_inch_leafon_bulk_release"])

 def test_tracker_endpoint_requires_auth(self):
  with app.test_client() as client:
   self.assertEqual(client.get("/api/indiana-counties").status_code,401)
   with client.session_transaction() as sess:sess["owner"]=True
   resp=client.get("/api/indiana-counties")
   self.assertEqual(resp.status_code,200)
   self.assertEqual(len(resp.json["county_rows"]),92)
   self.assertEqual(resp.json["county_audits_completed"],0)
   self.assertEqual(resp.json["county_2026_three_inch_bulk_release_count"],9)

 def test_hamilton_source_serves_with_provider_metadata(self):
  # Non-decodable mocked image is accepted only by the magic-byte/length guard;
  # service availability and real photo sharpness require a separate live QA.
  with app.test_client() as client:
   with client.session_transaction() as sess:sess["owner"]=True
   good=Mock(content=bytes.fromhex("ffd8")+b"0"*7000,raise_for_status=Mock())
   with patch("app.http.get",return_value=good) as req:
    resp=client.get("/api/aerial",query_string={
      "lat":"40.058","lon":"-86.055","state":"IN","county_fips":"18057",
      "bbox":"-86.056,40.057,-86.054,40.059","width":"1100","height":"1100"})
    self.assertEqual(resp.status_code,200)
    self.assertIn("Hamilton",resp.headers["X-Imagery-Source"])
    self.assertEqual(resp.headers["X-Imagery-Native-Inches"],"3")
    self.assertIn("Indiana_County_Collect_2024",req.call_args.args[0])

 def test_registry_reports_eight_curated_states(self):
  self.assertEqual(coverage_summary()["states_with_curated_regional_sources"],8)

if __name__=="__main__":unittest.main()
