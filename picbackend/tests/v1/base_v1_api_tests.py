"""
Defines base classes that tests for version 1 inherit from
"""


from django.test import Client
import json


class BaseV1RqstTests(object):
    base_url = "/v1/"
    client_object = Client()

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
        self.assertEqual(response_data["Status"]["Version"], 1.0)


class BaseV1APITests(BaseV1RqstTests):
    def test_fetch_all_objects_request(self):
        response = self.client_object.get(self.base_url)
        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        self.assertNotIn("Errors", response_data["Status"])
        self.assertEqual(response_data["Status"]["Error Code"], 0)
        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)


class BaseConsumerStaffMetricsTests(BaseV1APITests):

    def test_fetch_all_objects_request(self):
        self.base_url += "id=all"
        super(BaseConsumerStaffMetricsTests, self)
