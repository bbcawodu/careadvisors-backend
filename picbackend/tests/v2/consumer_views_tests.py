"""
Defines tests for version 2 of the consumer API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseConsumerNavigatorsMetricsTests
import json


class ConsumerAPITests(TestCase, BaseConsumerNavigatorsMetricsTests):
    def setUp(self):
        self.base_url += "consumers/"

    def test_add_consumer_view(self):
        post_data = {
            "first_name": "Johnsafsa",
            "middle_name": "",
            "last_name": "Consumerfasfsa",
            "gender": "female",
            "email": "",
            "phone": "",
            "met_nav_at": "Mariano's Bridgeport",
            "household_size": 3,
            "plan": "",
            "preferred_language": "",
            "consumer_notes": [
            ],

            "address_line_1": "",
            "address_line_2": "",
            "city": "",
            "state_province": "",
            "zipcode": "",

            "date_met_nav": {
                "Day": 31,
                "Month": 10,
                "Year": 2018,
            },
            # "navigator_id": 1,
            "cm_client_id_for_routing": 1,

            'add_referring_cm_clients': [
                1
            ],

            "db_action": "create"
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

        consumer_data = response_data["Data"]

        self.assertIn("row", consumer_data)
        self.assertEqual(consumer_data['row']['gender'], "female")
        self.assertEqual(consumer_data['row']['cm_client_for_routing'], "Client One")
        self.assertEqual(len(consumer_data['row']["referring_cm_clients"]), 1)

    def test_update_consumer_view(self):
        post_data = {
            "first_name": "Johnsaeqetsdbnjkfjhgjhgjhgjhgsa",
            "middle_name": "",
            "last_name": "Consumerfasfsa",
            "gender": "male",
            "email": "",
            "phone": "",
            "met_nav_at": "Mariano's Bridgeport",
            "household_size": 3,
            "plan": "",
            "preferred_language": "",
            "consumer_notes": [
            ],

            "address_line_1": "",
            "address_line_2": "",
            "city": "",
            "state_province": "",
            "zipcode": "",

            "date_met_nav": {
                "Day": 31,
                "Month": 10,
                "Year": 2018,
            },
            "navigator_id": None,
            "cm_client_id_for_routing": 1,

            'add_referring_cm_clients': [
                1
            ],

            "id": 1,
            "db_action": "update"
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

        consumer_data = response_data["Data"]

        self.assertIn("row", consumer_data)
        self.assertEqual(consumer_data['row']['gender'], "male")
        self.assertEqual(consumer_data['row']['cm_client_for_routing'], "Client One")
        self.assertEqual(consumer_data['row']['navigator'], None)
        self.assertEqual(len(consumer_data['row']["referring_cm_clients"]), 1)

    def test_add_cps_consumer_view(self):
        post_data = {
            "first_name": "Johnsafsddsa",
            "middle_name": "",
            "last_name": "Consumerfasfsa",
            "email": "",
            "phone": "",
            "met_nav_at": "Mariano's Bridgeport",
            "household_size": 3,
            "plan": "",
            "preferred_language": "",
            "consumer_notes": [
            ],

            "address_line_1": "",
            "address_line_2": "",
            "city": "",
            "state_province": "",
            "zipcode": "",

            "date_met_nav": {
                "Day": 31,
                "Month": 10,
                "Year": 2018,
            },

            "cps_consumer": True,
            "cps_info": {
                "primary_dependent": {
                    "first_name": "Kensdgset",
                    "last_name": "Massdgdsfsdeters",
                    # "Consumer Database ID": 134,
                },
                "cps_location": "Marquette Elementary School",
                "apt_date": {
                    "Day": 22,
                    "Month": 2,
                    "Year": 2017,
                },
                "target_list": True,
                "phone_apt": True,
                "case_mgmt_type": "String",
                "case_mgmt_status": "Open",
                "secondary_dependents": [
                    {
                        "first_name": "Brstdsdyan",
                        "last_name": "Furgsdfdsy",
                        # "Consumer Database ID": 135,
                    },
                ],
                "app_type": "SNAP",
                "app_status": "Pending",
                "point_of_origin": "Not Available"
            },

            "navigator_id": 1,
            "db_action": "create"
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
        consumer_data = response_data["Data"]

        self.assertIn("row", consumer_data)
