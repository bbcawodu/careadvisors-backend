from django.test import TestCase
import json


class EligibilityViewTests(TestCase):
    def setUp(self):
        self.post_data = {"Birth Date": None,
                          "First Name": None,
                          "Last Name": None,
                          "Trading Partner ID": None,
                          "Consumer Plan ID": None}

    def tearDown(self):
        del self.post_data

    def test_valid_user_elig_with_united_health_care(self):
        self.post_data["Birth Date"] = "1989-05-01"
        self.post_data["First Name"] = "Nicole"
        self.post_data["Last Name"] = "Mahan"
        self.post_data["Trading Partner ID"] = "united_health_care"
        json_post_data = json.dumps(self.post_data)

        response = self.client.post('/v1/eligibility/', json_post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response_data_json = response.content.decode('utf-8')
        response_data = json.loads(response_data_json)

        status_data = response_data["Status"]
        self.assertEqual(status_data["Version"], 1.0)
        self.assertEqual(status_data["Error Code"], 0)
        self.assertNotIn("Errors", status_data)
