import unittest
from mock import patch

class PopitOneTimeTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_data_messager(self):
        
        """Test for data_messager"""
        
        from popit.popit_json_importer import data_messager
        from popit import popit_json_importer
        input_data = {}
        input_data["birth_date"] = "1974-01-01"
        input_data["death_date"] = None
        input_data["end_date"] = "Some other date"
        input_data["founding_date"] = "2000"
        result = data_messager(input_data, "links")
        expected_result = {'birth_date': '1974-01-01',
                           'founding_date': '2000',
                           'death_date': '0000-00-00', 
                           'end_date': '0000-00-00'}
        
        self.assertEqual(result, expected_result)