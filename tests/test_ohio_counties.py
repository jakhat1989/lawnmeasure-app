"""Ohio 88-county OSIP routing and individual QA status."""
import unittest
from ohio_imagery import OHIO_COUNTIES, OHIO_SPECIAL, ohio_county_info, ohio_summary
from imagery_registry import SOURCES,select_government_sources
from app import app

class OhioTests(unittest.TestCase):
 def test_all_88_counties_complete_and_fips_codes(self):
  self.assertEqual(len(OHIO_COUNTIES),88)
  self.assertEqual(sorted(OHIO_COUNTIES),[f"39{i:03d}" for i in range(1,176,2)])
  self.assertEqual(OHIO_COUNTIES["39089"],"Licking")
  self.assertEqual(OHIO_COUNTIES["39151"],"Stark")

 def test_licking_2025_three_inch_is_selected_first(self):
  route=select_government_sources("OH",40.1,-82.45,"39089")
  self.assertEqual(route[0],"OH_LICKING_2025")
  self.assertIn("OH_OSIP_DYNAMIC",route)
  self.assertEqual(SOURCES[route[0]][3],3)

 def test_stark_has_county_specific_frontend_cache(self):
  row=ohio_county_info("39151")
  self.assertEqual(row["county_preferred_source"],"OH_STARK_2025")
  self.assertEqual(row["candidate_native_inches"],6)

 def test_other_counties_use_official_statewide_tiles(self):
  for fips in OHIO_COUNTIES:
   row=ohio_county_info(fips)
   self.assertFalse(row["county_completed"])
   self.assertEqual(row["fips"],fips)
   self.assertIn("maps.ohio.gov",row["statewide_source_url"])
   route=select_government_sources("OH",39.5,-83.5,fips)
   self.assertEqual(route[-2:],["USGS_PLUS","USGS_NAIP"])
  self.assertEqual(ohio_summary()["county_audits_completed"],0)

 def test_county_status_api_authenticated_only(self):
  with app.test_client() as c:
   self.assertEqual(c.get("/api/ohio-counties").status_code,401)
   with c.session_transaction() as session:
    session["owner"]=True
   response=c.get("/api/ohio-counties")
   self.assertEqual(response.status_code,200)
   self.assertEqual(response.json["county_count"],88)
   self.assertEqual(len(response.json["county_rows"]),88)
   self.assertEqual(response.json["county_audits_completed"],0)

 def test_image_endpoint_avoids_old_dynamic_overlay_on_licking(self):
  from unittest.mock import patch
  from unittest.mock import Mock
  good=b"\xff\xd8"+b"\x00"*7000
  with app.test_client() as c:
   with c.session_transaction() as session:session["owner"]=True
   with patch("app.http.get",return_value=Mock(content=good,raise_for_status=Mock())) as get:
    resp=c.get("/api/aerial",query_string={
     "lat":"40.1","lon":"-82.4","state":"OH","county_fips":"39089",
     "local_only":"1","bbox":"-82.401,40.099,-82.399,40.101",
     "width":1024,"height":1024})
    self.assertEqual(resp.status_code,200)
    self.assertIn("Licking",resp.headers["X-Imagery-Source"])
    self.assertIn("apps.lickingcounty.gov",get.call_args.args[0])

if __name__=="__main__":unittest.main()
