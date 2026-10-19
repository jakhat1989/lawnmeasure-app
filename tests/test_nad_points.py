import unittest
from unittest.mock import patch
import app

class MockResponse:
    def __init__(self, features):
        self.features = features
    def raise_for_status(self):
        return None
    def json(self):
        return {"features": self.features}

def item(house=123, street="Oak Street", placement="Structure - Rooftop",
         lat=39.0701, lon=-84.7201, zip_code="41001"):
    return {"geometry":{"x":lon,"y":lat},"attributes":{
        "Add_Number":house,"StNam_Full":street,
        "State":"KY","Zip_Code":zip_code,
        "Placement":placement,"Lifecycle":"Active"
    }}

class PinTests(unittest.TestCase):
    address="123 Oak St, Sampletown, KY, 41001"
    def check(self, features):
        with patch.object(app.http,"get",return_value=MockResponse(features)):
            return app.nad_address_point(self.address,39.0700,-84.7200)

    def test_rooftop_address_point(self):
        result=self.check([item()])
        self.assertEqual(result["pin_accuracy"],"rooftop_recorded")
        self.assertAlmostEqual(result["lat"],39.0701)

    def test_wrong_house_is_rejected(self):
        self.assertIsNone(self.check([item(house=125)]))

    def test_wrong_street_is_rejected(self):
        self.assertIsNone(self.check([item(street="Pine St")]))

    def test_wrong_zip_is_rejected(self):
        self.assertIsNone(self.check([item(zip_code="41002")]))

    def test_far_point_is_rejected(self):
        self.assertIsNone(self.check([item(lat=39.09,lon=-84.72)]))

    def test_non_rooftop_never_called_rooftop(self):
        result=self.check([item(placement="Structure - Entrance")])
        self.assertEqual(result["pin_accuracy"],"address_point")

    def test_missing_address_has_no_result(self):
        self.assertIsNone(self.check([]))

if __name__=="__main__":
    unittest.main()
