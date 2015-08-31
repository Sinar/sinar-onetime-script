import unittest
import json
from mock import patch, Mock


class PopitOneTimeTests(unittest.TestCase):

    def setUp(self):
        input_data = dict(
            birth_date="1974-01-01",
            death_date= None,
            end_date="Some other date",
            founding_date="2000",
            url="http://www.testurl.com",
            html_url="http://www.htmlurl.com",
            area=dict(id="12345"))
        self.input_data = input_data

    def tearDown(self):
        pass

    def mock_response(self, data, headers, status_code=200):

        response = Mock
        response.status_code = status_code
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
                           'end_date': '0000-00-00',
                           'url': 'http://www.testurl.com',
                           'html_url': 'http://www.htmlurl.com',
                           'area':
                               {'id': '12345'}}

        self.assertEqual(result, expected_result)
        for item in ('url', 'html_url'):
            self.assertIn(item, result)

        result_no_links = data_messager(self.input_data, "area")
        for item in ('url', 'html_url'):
            self.assertNotIn(item, result_no_links)

        self.assertIn('area', result_no_links)


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
