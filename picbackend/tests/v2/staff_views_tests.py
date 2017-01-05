"""
Defines tests for version 2 of the staff API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseConsumerStaffMetricsTests
import json


class StaffAPITests(TestCase, BaseConsumerStaffMetricsTests):
    def setUp(self):
        self.base_url += "staff/"

    def test_add_staff_view(self):
        post_data = {
            "First Name": "sdfdsfafassadr",
            "Last Name": "Marlsasdfsdfdsfdsfdda",
            "Email": "donadsfdsfa@patfdsfdie.org",
            "User Type": "Navigator",
            "User County": "Montgomery",
            "MPN": "Cook",
            "Base Locations": ['Lincoln Belmont Library', 'Thorek Memorial Hospital'],
            "Database Action": "Staff Addition",
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

        # Test decoded JSON data for non empty "Next Available Appointments" data
        staff_data = response_data["Data"]

        self.assertIn("Database ID", staff_data)
