"""Top-50 metropolitan imagery target classification regression tests."""
import unittest
from unittest.mock import patch, Mock
from metro_imagery import TOP_50_METROS, METRO_RANKING_2025, find_top_metro, metro_summary
from app import app, metro_at_location

class MetroPriorityTests(unittest.TestCase):
 def test_ranked_50_true_metros(self):
  self.assertEqual(len(TOP_50_METROS),50)
  self.assertEqual([row["rank"] for row in TOP_50_METROS],list(range(1,51)))
  self.assertEqual(len({name for name,_ in METRO_RANKING_2025}),50)
  self.assertTrue(all(x["population_2025"]>y["population_2025"]
    for x,y in zip(TOP_50_METROS,TOP_50_METROS[1:])))
  self.assertEqual(TOP_50_METROS[0]["name"],"New York-Newark-Jersey City, NY-NJ")
  self.assertEqual(TOP_50_METROS[-1]["name"],"Hartford-West Hartford-East Hartford, CT")

 def test_suburban_metro_name_variant(self):
  match=find_top_metro("Cincinnati, OH-KY-IN","17140")
  self.assertTrue(match["target"])
  self.assertEqual(match["rank"],30)
  # Several secondary principal cities have been renamed since July 2025.
  self.assertEqual(find_top_metro("Indianapolis-Carmel-Anderson, IN")["rank"],33)

 def test_ambiguous_city_names_require_correct_state(self):
  self.assertIsNone(find_top_metro("Portland-South Portland, ME"))
  self.assertIsNone(find_top_metro("Columbus, GA-AL"))
  self.assertIsNone(find_top_metro("Jacksonville, NC"))

 def test_census_geography_metro_saves_network_lookup(self):
  geography={"Metropolitan Statistical Areas":[{
    "BASENAME":"Chicago-Naperville-Elgin, IL-IN",
    "GEOID":"16980"}]}
  with patch("app.http.get") as req:
   result=metro_at_location(41.9,-87.8,geography)
  self.assertEqual(result["rank"],3)
  req.assert_not_called()

 def test_polygon_query_identifies_suburb_through_official_metro_boundary(self):
  response=Mock()
  response.raise_for_status=Mock()
  response.json.return_value={"features":[{
   "attributes":{"BASENAME":"Cincinnati, OH-KY-IN","GEOID":"17140"}}]}
  with patch("app.http.get",return_value=response) as fetch:
   result=metro_at_location(39.05,-84.7,{})
  self.assertEqual(result["rank"],30)
  self.assertTrue(result["target"])
  self.assertIn("tigerweb.geo.census.gov",fetch.call_args.args[0])
  self.assertEqual(fetch.call_args.kwargs["params"]["geometryType"],"esriGeometryPoint")

 def test_non_top_50_returns_not_target_not_false_rank(self):
  geography={"Metropolitan Statistical Areas":[{"BASENAME":"Tucson, AZ","GEOID":"46060"}]}
  result=metro_at_location(32.22,-110.9,geography)
  self.assertFalse(result["target"])
  self.assertEqual(result["name"],"Tucson, AZ")

 def test_unavailable_boundary_lookup_is_unknown_not_outside(self):
  import requests
  with patch("app.http.get",side_effect=requests.Timeout()):
   result=metro_at_location(39,-86,{})
  self.assertIsNone(result["target"])

 def test_tracker_requires_owner_login(self):
  with app.test_client() as client:
   self.assertEqual(client.get("/api/top-metros").status_code,401)
   with client.session_transaction() as session:session["owner"]=True
   response=client.get("/api/top-metros")
   self.assertEqual(response.status_code,200)
   self.assertEqual(len(response.json["metros"]),50)
   self.assertEqual(response.json["metro_qa_completed"],0)
   self.assertIn("suburbs",response.json["metro_definition"])

 def test_metro_priority_registry_does_not_claim_photos_audited(self):
  self.assertEqual(metro_summary()["metro_qa_completed"],0)
  self.assertTrue(all(not row["metro_image_qa_complete"] for row in TOP_50_METROS))
  self.assertTrue(all(not row["county_and_suburb_coverage_audited"] for row in TOP_50_METROS))

if __name__=="__main__":unittest.main()
