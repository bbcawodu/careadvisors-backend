"""
Defines tests for version 2 of the navigator hub locations API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseV2APITests
import json


class NavHubLocationAPITests(TestCase, BaseV2APITests):
    def setUp(self):
        self.base_url += "navigator_hub_locations/"

    def test_add_or_update_nav_hub_location_view(self):
        post_data = {
                      "Location Name": "Mariano's Bridgeport",
                      "Address Line 1": "3145 S Ashland Ave",
                      "Address Line 2": "",
                      "City": "Chicago",
                      "State": "IL",
                      "Zipcode": "60608",
                      "Country": "United States of America",

                      "Database Action": "Location Addition"
                      }

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
