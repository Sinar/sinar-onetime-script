import unittest
import json
from mock import patch, Mock


class PopitOneTimeTests(unittest.TestCase):

    def setUp(self):
        input_data = {}
        input_data["birth_date"] = "1974-01-01"
        input_data["death_date"] = None
        input_data["end_date"] = "Some other date"
        input_data["founding_date"] = "2000"
        self.input_data = input_data

    def tearDown(self):
        pass

    def mock_response(self, data, headers):

        response = Mock
        response.status_code = 200
        response.data = data
        response.headers = headers
        return response

    def test_data_messager(self):

        """Test for data_messager"""

        from popit.popit_json_importer import data_messager
        result = data_messager(self.input_data, "links")
        expected_result = {'birth_date': '1974-01-01',
                           'founding_date': '2000',
                           'death_date': '0000-00-00',
                           'end_date': '0000-00-00'}

        self.assertEqual(result, expected_result)

    @patch("popit.popit_json_importer.requests.post", mock_response)
    @patch("popit.popit_json_importer.data_messager")
    def test_create_entity(self, mock_data_m):

        """Test for create_entity"""

        from popit.popit_json_importer import data_messager, create_entity
        result = data_messager(self.input_data, "links")
        mock_data_m.return_value = e_data = {'birth_date': '1974-01-01',
                                             'founding_date': '2000',
                                             'death_date': '0000-00-00',
                                             'end_date': '0000-00-00'}
        create_entity(self.input_data, "123",
                      "birth_date", "test_api_key")
        expected_header = {'Apikey': 'test_api_key',
                           'Content-Type': 'application/json'}
        self.assertEqual(expected_header, result.headers)
        self.assertEqual(json.dumps(e_data), result.data)
