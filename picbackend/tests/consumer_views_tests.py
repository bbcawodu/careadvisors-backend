from picbackend.tests.base import BaseWithDBTests
from django.test import TestCase, Client
import json


class ConsumerAPITests(BaseWithDBTests):
    def setUp(self):
        self.base_url = "/v1/staff/?"
        self.client_object = Client()

    def test_for_ok_response_code(self):
        get_url = self.base_url + "id=all"
        response = self.client_object.get(get_url)

        self.assertEqual(response.status_code, 200)

    def test_for_decoded_response_data(self):
        get_url = self.base_url + "id=all"
        response = self.client_object.get(get_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertIsNotNone(response_data)

    def test_for_status_data(self):
        get_url = self.base_url + "id=all"
        response = self.client_object.get(get_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertIsNotNone(response_data["Status"])

    def test_status_data_for_correct_version(self):
        get_url = self.base_url + "id=all"
        response = self.client_object.get(get_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertEqual(response_data["Status"]["Version"], 1.0)

    def test_status_data_for_valid_error_code(self):
        get_url = self.base_url + "id=all"
        response = self.client_object.get(get_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertEqual(response_data["Status"]["Error Code"], 0)

    def test_status_data_has_no_error_msgs(self):
        get_url = self.base_url + "id=all"
        response = self.client_object.get(get_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertNotIn("Errors", response_data["Status"])

    def test_id_all_request(self):
        get_url = self.base_url + "id=all"
        response = self.client_object.get(get_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)
