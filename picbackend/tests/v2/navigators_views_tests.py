from django.test import TestCase
from .base_v2_api_tests import BaseConsumerNavigatorsMetricsTests
from .base_v2_api_tests import BaseV2RqstTests
import json


class NavigatorAPITests(TestCase, BaseConsumerNavigatorsMetricsTests):
    def setUp(self):
        self.base_url += "navigators/"

    def test_add_navigator_view(self):
        post_data = {
            "first_name": "sdfdsfafassadr",
            "last_name": "Marlsasdfsdfdsfdsfdda",
            "email": "donadsfdsfa@patfdsfdie.org",
            "type": "Navigator",
            "county": "Montgomery",
            "mpn": "Cook",
            "add_base_locations": ['Lincoln Belmont Library', 'Thorek Memorial Hospital'],

            'add_healthcare_locations_worked': [
                {
                    'name': 'Edward Hospital & Immediate Careasdss',
                    'state_province': 'not available'
                }
            ],
            'add_healthcare_service_expertises': [
                'bariatrics',
            ],
            'add_insurance_carrier_specialties': [
                {
                    'name': 'Health Alliance Medical Plans, Inc.',
                    'state_province': 'il'
                },
            ],

            "create_resume_row": {
                "profile_description": "apple",
                "create_education_rows": [
                    {
                        "school": "easy",
                        "major": "peasy",
                        "degree_type": "masters"
                    },
                    {
                        "school": "lemon",
                        "major": "squeezy",
                        "degree_type": "masters"
                    },
                ],
                "create_job_rows": [
                    {
                        "title": "easy",
                        "company": "peasy",
                        "description": "masters"
                    },
                    {
                        "title": "lemon",
                        "company": "squeezy",
                        "description": "masters"
                    },
                ],
            },

            "address_line_1": "",
            "address_line_2": "",
            "city": "",
            "state_province": "",
            "zipcode": "",

            "phone": "2813307004",
            "reported_region": "cook",
            "video_link": "https://www.twitch.tv/videos/239858398",
            "navigator_organization": "sljidsjflksa",

            "db_action": "create",
        }

        post_json = json.dumps(post_data)
        response = self.client_object.put(self.base_url, post_json, content_type="application/json")

        # Test for a valid reponse code (200)
        self.assertEqual(response.status_code, 200)

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

        self.assertIn("row", staff_data)
        if "row" in staff_data:
            db_row = staff_data['row']

            self.assertEqual(
                db_row['first_name'],
                post_data['first_name'],
                "row name: {}, request name: {}".format(db_row['first_name'], post_data['first_name'])
            )
            self.assertEqual(
                len(db_row['base_locations']),
                2,
                "row base locations count: {}".format(len(db_row['base_locations']))
            )
            self.assertEqual(
                len(db_row['healthcare_locations_worked']),
                1,
                "row healthcare_locations_worked count: {}".format(len(db_row['healthcare_locations_worked']))
            )
            self.assertEqual(
                len(db_row['insurance_carrier_specialties']),
                1,
                "row insurance_carrier_specialties count: {}".format(len(db_row['insurance_carrier_specialties']))
            )
            self.assertEqual(
                len(db_row['healthcare_service_expertises']),
                1,
                "row healthcare_service_expertises count: {}".format(len(db_row['healthcare_service_expertises']))
            )
            self.assertEqual(
                len(db_row['resume_info']),
                1,
                "row resume count: {}".format(len(db_row['resume_info']))
            )


class NavigatorSignUpAPITests(TestCase, BaseV2RqstTests):
    def setUp(self):
        self.base_url += "navigator_sign_up/"

    def test_add_navigator_view(self):
        post_data = {
            "first_name": "sdfdsfafassadr",
            "last_name": "Marlsasdfsdfdsfdsfdda",
            "email": "donadsfdsfa@patfdsfdie.org",

            'add_healthcare_locations_worked': [
                {
                    'name': 'Edward Hospital & Immediate Careasdss',
                    'state_province': 'not available'
                }
            ],
            'add_healthcare_service_expertises': [
                'bariatrics',
            ],
            'add_insurance_carrier_specialties': [
                {
                    'name': 'Health Alliance Medical Plans, Inc.',
                    'state_province': 'il'
                },
            ],

            "create_resume_row": {
                "profile_description": "apple",
                "create_education_rows": [
                    {
                        "school": "easy",
                        "major": "peasy",
                        "degree_type": "masters"
                    },
                    {
                        "school": "lemon",
                        "major": "squeezy",
                        "degree_type": "masters"
                    },
                ],
                "create_job_rows": [
                    {
                        "title": "easy",
                        "company": "peasy",
                        "description": "masters"
                    },
                    {
                        "title": "lemon",
                        "company": "squeezy",
                        "description": "masters"
                    },
                ],
            },

            "address_line_1": "",
            "address_line_2": "",
            "city": "",
            "state_province": "",
            "zipcode": "",

            "phone": "2813307004",
            "reported_region": "cook",
            "video_link": "https://www.twitch.tv/videos/239858398",

            "db_action": "create",
        }

        post_json = json.dumps(post_data)
        response = self.client_object.put(self.base_url, post_json, content_type="application/json")

        # Test for a valid reponse code (200)
        self.assertEqual(response.status_code, 200)

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

        self.assertIn("row", staff_data)
        if "row" in staff_data:
            db_row = staff_data['row']

            self.assertEqual(
                db_row['first_name'],
                post_data['first_name'],
                "row name: {}, request name: {}".format(db_row['first_name'], post_data['first_name'])
            )
            self.assertEqual(
                len(db_row['base_locations']),
                0,
                "row base locations count: {}".format(len(db_row['base_locations']))
            )
            self.assertEqual(
                len(db_row['healthcare_locations_worked']),
                1,
                "row healthcare_locations_worked count: {}".format(len(db_row['healthcare_locations_worked']))
            )
            self.assertEqual(
                len(db_row['insurance_carrier_specialties']),
                1,
                "row insurance_carrier_specialties count: {}".format(len(db_row['insurance_carrier_specialties']))
            )
            self.assertEqual(
                len(db_row['healthcare_service_expertises']),
                1,
                "row healthcare_service_expertises count: {}".format(len(db_row['healthcare_service_expertises']))
            )
            self.assertEqual(
                len(db_row['resume_info']),
                1,
                "row resume count: {}".format(len(db_row['resume_info']))
            )
