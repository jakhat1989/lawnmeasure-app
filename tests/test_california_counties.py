"""California 58-county and published aerial imagery provider routing tests."""
import unittest
from unittest.mock import patch, Mock
from california_imagery import CALIFORNIA_COUNTIES, california_summary, california_county_info
from imagery_registry import SOURCES,select_government_sources,coverage_summary
from app import app

class CaliforniaImageryTests(unittest.TestCase):
 def test_58_official_counties_and_FIPS(self):
  self.assertEqual(len(CALIFORNIA_COUNTIES),58)
  self.assertEqual(sorted(CALIFORNIA_COUNTIES),[f"06{n:03d}" for n in range(1,116,2)])
  self.assertEqual(CALIFORNIA_COUNTIES["06055"],"Napa")
  self.assertEqual(CALIFORNIA_COUNTIES["06073"],"San Diego")
  self.assertEqual(CALIFORNIA_COUNTIES["06037"],"Los Angeles")

 def test_napa_2025_near_three_inches_prioritized(self):
  ids=select_government_sources("CA",38.3,-122.3,"06055")
  self.assertEqual(ids[0],"CA_NAPA_2025")
  self.assertEqual(ids[1],"CA_CDFW_NAIP_2022")
  self.assertLess(SOURCES[ids[0]][3],3.1)

 def test_san_diego_prioritizes_public_newer_2023_nine_inch(self):
  ids=select_government_sources("CA",32.78,-117.13,"06073")
  self.assertEqual(ids[:3],["CA_SAN_DIEGO_2023_9IN","CA_SAN_DIEGO_2017_4IN","CA_CDFW_NAIP_2022"])
  self.assertEqual(SOURCES[ids[0]][3],9)

 def test_statewide_baseline_not_mislabeled_three_inch(self):
  for fips in CALIFORNIA_COUNTIES:
   ids=select_government_sources("CA",37.0,-120.0,fips)
   self.assertIn("CA_CDFW_NAIP_2022",ids)
   self.assertEqual(ids[-2:],["USGS_PLUS","USGS_NAIP"])
   self.assertFalse(california_county_info(fips)["county_completed"])
  self.assertGreater(SOURCES["CA_CDFW_NAIP_2022"][3],20)

 def test_census_fips_unavailable_uses_conservative_city_fallback(self):
  self.assertEqual(select_government_sources("CA",38.297,-122.288)[0],"CA_NAPA_2025")
  self.assertEqual(select_government_sources("CA",32.77,-117.18)[0],"CA_SAN_DIEGO_2023_9IN")
  self.assertEqual(select_government_sources("CA",37.8,-119.5)[0],"CA_CDFW_NAIP_2022")

 def test_LA_restricted_landcover_never_activated(self):
  row=california_county_info("06037")
  self.assertTrue(row["restricted_or_unverified_higher_resolution"])
  self.assertEqual(row["preferred_county_source"],"CA_CDFW_NAIP_2022")
  self.assertFalse(any(k.startswith("CA_LARIAC7") for k in SOURCES))

 def test_tracker_requires_auth(self):
  with app.test_client() as client:
   self.assertEqual(client.get("/api/california-counties").status_code,401)
   with client.session_transaction() as sess:sess["owner"]=True
   response=client.get("/api/california-counties")
   self.assertEqual(response.status_code,200)
   self.assertEqual(len(response.json["county_rows"]),58)
   self.assertEqual(response.json["county_audits_completed"],0)
   self.assertEqual(response.json["county_specific_sources_configured"],2)

 def test_napa_aerial_source_response_header(self):
  # Mock byte size/magic. This tests backend routing, not live image clarity.
  with app.test_client() as client:
   with client.session_transaction() as sess:sess["owner"]=True
   fake=Mock(content=bytes.fromhex("ffd8")+b"0"*7000,raise_for_status=Mock())
   with patch("app.http.get",return_value=fake) as get:
    r=client.get("/api/aerial",query_string={
      "lat":"38.297","lon":"-122.29","state":"CA","county_fips":"06055",
      "bbox":"-122.291,38.296,-122.289,38.298","width":"1000","height":"1000"})
    self.assertEqual(r.status_code,200)
    self.assertEqual(r.headers["X-Imagery-Native-Inches"],"2.94")
    self.assertIn("Napa",r.headers["X-Imagery-Source"])
    self.assertIn("gis.napa.ca.gov",get.call_args.args[0])

 def test_nine_curated_states_now(self):
  self.assertEqual(coverage_summary()["states_with_curated_regional_sources"],9)

if __name__=="__main__":unittest.main()
