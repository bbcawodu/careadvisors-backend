"""
Defines tests for version 1 of the patient assist consumer appointment scheduler API for the picbackend app
"""


from django.test import TestCase
from .base_v1_api_tests import BaseV1RqstTests
import json


class PatientAssistSchedulerAPITests(TestCase, BaseV1RqstTests):
    def setUp(self):
        self.base_url += "getnavappointments/"

    def test_view_next_available_navigator_appointments(self):
        post_data = {"Preferred Times": [],}
        post_json = json.dumps(post_data)
        response = self.client_object.post(self.base_url, post_json, content_type="application/json")
        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 1.0)

        status_data = response_data["Status"]

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(status_data)

        # Test decoded JSON data for non empty "Next Available Appointments" data
        next_available_appointment_data = response_data["Data"]["Next Available Appointments"]
        self.assertNotEqual(len(next_available_appointment_data), 0)

        preferred_appointments_data = response_data["Data"]["Preferred Appointments"]

        # Test that length of "Preferred Appointments" in decoded JSON data is equal to length of request
        # "Preferred Times" list
        self.assertEqual(len(preferred_appointments_data), len(post_data["Preferred Times"]))

        # Test decoded JSON data for empty "Preferred Appointments" data
        self.assertEqual(len(preferred_appointments_data), 0)

    def test_view_preferred_navigator_appointments(self):
        post_data = {"Preferred Times": ["2017-01-04T20:00:00"],}
        post_json = json.dumps(post_data)
        response = self.client_object.post(self.base_url, post_json, content_type="application/json")
        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 1.0)

        status_data = response_data["Status"]

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(status_data)

        # Test decoded JSON data for non empty "Next Available Appointments" data
        next_available_appointment_data = response_data["Data"]["Next Available Appointments"]
        self.assertEqual(len(next_available_appointment_data), 0)

        preferred_appointments_data = response_data["Data"]["Preferred Appointments"]

        # Test that length of "Preferred Appointments" in decoded JSON data is equal to length of request
        # "Preferred Times" list
        self.assertEqual(len(preferred_appointments_data), len(post_data["Preferred Times"]))

        # Test decoded JSON data for non empty preferred appointment
        self.assertNotEqual(len(preferred_appointments_data[0]), 0)
