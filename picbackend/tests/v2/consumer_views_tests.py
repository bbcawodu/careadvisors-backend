"""
Defines tests for version 2 of the consumer API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseConsumerStaffMetricsTests
import json


class ConsumerAPITests(TestCase, BaseConsumerStaffMetricsTests):
    def setUp(self):
        self.base_url += "consumers/"

    def test_add_consumer_view(self):
        post_data = {"First Name": "Johnsafsa",
                     "Middle Name": "",
                     "Last Name": "Consumerfasfsa",
                     "Email": "",
                     "Phone Number": "",
                     "Met Navigator At": "Mariano's Bridgeport",
                     "Household Size": 3,
                     "Plan": "",
                     "Preferred Language": "",
                     "Navigator Notes": [
                     ],

                     "Address Line 1": "",
                     "Address Line 2": "",
                     "City": "",
                     "State": "",
                     "Zipcode": "",

                     "date_met_nav": {"Day": 31,
                                      "Month": 10,
                                      "Year": 2018,
                                      },
                     "Navigator Database ID": 1,
                     "Database Action": "Consumer Addition",}

        post_json = json.dumps(post_data)
        response = self.client_object.put(self.base_url, post_json, content_type="application/json")
        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        status_data = response_data["Status"]

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(status_data)
        self.assertNotIn("Errors", status_data)
        self.assertEqual(status_data["Error Code"], 0)
        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)

        # Test decoded JSON data for correct API version
        self.assertEqual(status_data["Version"], 2.0)

        # Test decoded JSON data for non empty "Next Available Appointments" data
        consumer_data = response_data["Data"]

        self.assertIn("Database ID", consumer_data)
