"""
Defines tests for version 1 of the patient assist consumer appointment scheduler API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseV2RqstTests
import json


class PatientAssistSchedulerAPITests(TestCase, BaseV2RqstTests):
    def setUp(self):
        self.base_url += "patient_assist_apt_mgr/"

    def test_view_next_available_navigator_appointments(self):
        post_data = {"Preferred Times": [],}
        post_json = json.dumps(post_data)
        response = self.client_object.post(self.base_url, post_json, content_type="application/json")
        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 2.0)

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

        self.assertNotIn("Errors", status_data)
        self.assertEqual(status_data["Error Code"], 0)
        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)

    # def test_view_preferred_navigator_appointments(self):
    #     post_data = {"Preferred Times": ["2018-01-04T20:00:00"],}
    #     post_json = json.dumps(post_data)
    #     response = self.client_object.post(self.base_url, post_json, content_type="application/json")
    #     response_json = response.content.decode('utf-8')
    #     response_data = json.loads(response_json)
    #
    #     # Test for valid decoded json data from response body
    #     self.assertIsNotNone(response_data)
    #
    #     # Test decoded JSON data for correct API version
    #     self.assertEqual(response_data["Status"]["Version"], 2.0)
    #
    #     status_data = response_data["Status"]
    #
    #     # Test decoded JSON data for "Status" key
    #     self.assertIsNotNone(status_data)
    #
    #     # Test decoded JSON data for non empty "Next Available Appointments" data
    #     next_available_appointment_data = response_data["Data"]["Next Available Appointments"]
    #     self.assertEqual(len(next_available_appointment_data), 0)
    #
    #     preferred_appointments_data = response_data["Data"]["Preferred Appointments"]
    #
    #     # Test that length of "Preferred Appointments" in decoded JSON data is equal to length of request
    #     # "Preferred Times" list
    #     self.assertEqual(len(preferred_appointments_data), len(post_data["Preferred Times"]))
    #
    #     # Test decoded JSON data for non empty preferred appointment
    #     self.assertNotEqual(len(preferred_appointments_data[0]), 0)
    #
    #     self.assertNotIn("Errors", status_data)
    #     self.assertEqual(status_data["Error Code"], 0)
    #     self.assertIn("Data", response_data)
    #     self.assertNotEqual(len(response_data["Data"]), 0)

    def test_add_consumer_apt_with_nav(self):
        post_data = {"navigator_id": 1,
                     "Appointment Date and Time": '2018-03-08T16:00:00',

                     "Consumer Info": {
                                        "first_name": "calkfndy",
                                        "middle_name": "ljhvjhgjhgjhgoli",
                                        "last_name": "pophgfthcdfgcgh",
                                        "email": "niggmagician89@gmail.com",
                                        "phone": "2813308004",
                                        "household_size": 11,
                                        "plan": "String (Can be empty)",
                                        "preferred_language": "English",

                                        "address_line_1": "6540 N Glenwood",
                                        "address_line_2": "",
                                        "city": "",
                                        "state_province": "",
                                        "zipcode": ""
                                      }
                     }
        post_json = json.dumps(post_data)
        response = self.client_object.put(self.base_url, post_json, content_type="application/json")
        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 2.0)

        status_data = response_data["Status"]

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(status_data)

        self.assertNotIn("Errors", status_data)
        self.assertEqual(status_data["Error Code"], 0)
        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)

    def test_view_navigators_scheduled_appointments(self):
        self.base_url += "?nav_id=1"
        response = self.client_object.get(self.base_url)
        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 2.0)

        status_data = response_data["Status"]

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(status_data)

        self.assertNotIn("Errors", status_data)
        self.assertEqual(status_data["Error Code"], 0)
        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)

    def test_delete_consumer_apt_with_nav(self):
        post_data = {"Navigator ID": 1,
                     "Appointment Date and Time": '2018-03-08T16:00:00',
                     }
        post_json = json.dumps(post_data)
        response = self.client_object.delete(self.base_url, post_json, content_type="application/json")
        response_json = response.content.decode('utf-8')
        response_data = json.loads(response_json)

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 2.0)

        status_data = response_data["Status"]

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(status_data)

        self.assertNotIn("Errors", status_data)
        self.assertEqual(status_data["Error Code"], 0)
        self.assertIn("Data", response_data)
        self.assertNotEqual(len(response_data["Data"]), 0)
