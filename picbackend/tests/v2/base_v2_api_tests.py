"""
Defines base classes that tests for version 2 inherit from
"""


from django.test import Client
from django.conf import settings
import json


class BaseV2RqstTests(object):
    base_url = "/v2/"
    client_object = Client()
    settings.DEBUG = True

    def test_base_rqst(self):
        response = self.client_object.get(self.base_url)

        # Test for a valid reponse code (200)
        self.assertEqual(response.status_code, 200)

        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(response_data["Status"])

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 2.0)


class BaseV2APITests(BaseV2RqstTests):
    def test_base_fetch_all_objects_request(self):
        response = self.client_object.get(self.base_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertNotIn("Errors", response_data["Status"])
        self.assertEqual(response_data["Status"]["Error Code"], 0)
        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)


class BaseConsumerStaffMetricsTests(BaseV2APITests):

    def test_base_fetch_all_objects_request(self):
        self.base_url += "?id=all"

        super(BaseConsumerStaffMetricsTests, self).test_base_fetch_all_objects_request()
