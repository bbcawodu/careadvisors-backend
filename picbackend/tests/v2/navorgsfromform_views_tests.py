from django.test import TestCase
from .base_v2_api_tests import BaseConsumerNavigatorsMetricsTests
import json


class NavigatorAPITests(TestCase, BaseConsumerNavigatorsMetricsTests):
    def setUp(self):
        self.base_url += "nav_orgs_from_form/"

    def test_add_navigator_view(self):
        post_data = {
            "company_name": "Shithole Enterprises",

            "address_line_1": "dfjkhds",
            "address_line_2": "dslkds",
            "city": "sakjsa",
            "state_province": "TX",
            "zipcode": "29873",

            "estimated_monthly_caseload": 12345,
            "contact_first_name": "safassadssadtrerrsasdfews",
            "contact_last_name": "Marlsadsfdsfdda",
            "contact_email": "applemartini@gmail.com",
            "contact_phone": "2813307004",

            "appointment_datetime": "2018-05-03T17:00:00",


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
                db_row['company_name'],
                post_data['company_name'],
                "row name: {}, request name: {}".format(db_row['company_name'], post_data['company_name'])
            )
