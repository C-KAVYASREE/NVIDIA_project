import unittest
from pathlib import Path
from retrieval import WasteRetriever

class WasteRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = WasteRetriever(Path(__file__).resolve().parents[1]/"data"/"waste_knowledge.json")
    def test_dataset_has_twenty_records(self):
        self.assertEqual(len(self.r.records),20)
    def test_battery_retrieval(self):
        result=self.r.search("where should I throw away a used AA battery")
        self.assertTrue(result)
        self.assertIn("battery",result[0]["item"].lower())
    def test_mobile_phone_retrieval(self):
        result=self.r.search("old smartphone disposal")
        self.assertTrue(result)
        self.assertIn("phone",result[0]["item"].lower())
    def test_food_scraps_retrieval(self):
        result=self.r.search("banana peels and vegetable leftovers")
        self.assertTrue(result)
        self.assertIn("peel",result[0]["item"].lower())
    def test_all_records_have_source(self):
        self.assertTrue(all(x["source"].startswith("https://") for x in self.r.records))
if __name__=="__main__": unittest.main()
