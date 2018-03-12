"""
Defines tests for version 2 of the consumer metrics API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseConsumerStaffMetricsTests
import json


class ConsumerMetricsAPITests(TestCase, BaseConsumerStaffMetricsTests):
    def setUp(self):
        self.base_url += "metrics/"

    def test_add_or_update_metrics_view(self):
        post_data = {
            "Email": "tech@piccares.org",
            "Consumer Metrics": {
                "Metrics Date": {
                    "Day": 31,
                    "Month": 12,
                    "Year": 2017,
                },
                "Plan Stats": [],
                "County": "Cook",
                "Location": "Chicago Reed Mental Health Center",
                "no_general_assis": 0,
                "no_plan_usage_assis": 1,
                "no_locating_provider_assis": 2,
                "no_billing_assis": 3,
                "no_enroll_apps_started": 4,
                "no_enroll_qhp": 5,
                "no_enroll_abe_chip": 6,
                "no_enroll_shop": 7,
                "no_referrals_agents_brokers": 8,
                "no_referrals_ship_medicare": 9,
                "no_referrals_other_assis_programs": 10,
                "no_referrals_issuers": 11,
                "no_referrals_doi": 12,
                "no_mplace_tax_form_assis": 13,
                "no_mplace_exempt_assis": 14,
                "no_qhp_abe_appeals": 15,
                "no_data_matching_mplace_issues": 16,
                "no_sep_eligible": 17,
                "no_employ_spons_cov_issues": 18,
                "no_aptc_csr_assis": 19,
                "cmplx_cases_mplace_issues": "This is a court order not to eat shit."
            },
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

        # Test decoded JSON data for correct API version
        self.assertEqual(status_data["Version"], 2.0)
