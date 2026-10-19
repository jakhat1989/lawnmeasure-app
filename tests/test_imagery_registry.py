"""Coverage registry, county-aware source priority, and blank-image screening."""
import unittest
from io import BytesIO
from PIL import Image
from imagery_registry import STATE_CODES, SOURCES, coverage_summary, select_government_sources
from app import public_image_has_content

class CatalogTests(unittest.TestCase):
    def test_all_states_have_fallback(self):
        self.assertEqual(len(STATE_CODES),51)
        for state in STATE_CODES:
            ids=select_government_sources(state,39.2,-86.5)
            self.assertEqual(ids[-2:],["USGS_PLUS","USGS_NAIP"])
            self.assertTrue(all(k in SOURCES for k in ids))

    def test_county_override_cook(self):
        self.assertEqual(select_government_sources("IL",41.9,-87.7,"17031")[0],"IL_COOK")

    def test_county_override_marion(self):
        self.assertEqual(select_government_sources("FL",29.12,-82.03,"12083")[:2],
                         ["FL_MARION_2024","FL_MARION"])

    def test_maryland_prefers_three_inches(self):
        ids=select_government_sources("MD",39.1,-76.8,"24003")
        self.assertEqual(ids[:2],["MD_3IN","MD_6IN"])

    def test_north_carolina_latest_six_inches(self):
        self.assertEqual(select_government_sources("NC",35.7,-78.7)[0],"NC_LATEST")

    def test_illinois_block_priorities(self):
        self.assertIn("IL_2_EAST",select_government_sources("IL",40.3,-88.1)[:2])

    def test_public_coverage_not_falsely_complete(self):
        status=coverage_summary()
        self.assertEqual(status["county_audits_completed"],0)
        self.assertEqual(status["states_with_curated_regional_sources"],6)

    def test_blank_image_is_rejected(self):
        out=BytesIO()
        Image.new("RGB",(200,200),(255,255,255)).save(out,"JPEG")
        self.assertFalse(public_image_has_content(out.getvalue()))

    def test_varying_colors_are_accepted(self):
        out=BytesIO()
        image=Image.new("RGB",(200,200))
        image.putdata([(i%200,j%200,(i*j)%255) for j in range(200) for i in range(200)])
        image.save(out,"JPEG")
        self.assertTrue(public_image_has_content(out.getvalue()))

if __name__=="__main__":unittest.main()
