"""
Defines tests for version 2 of the consumer health insurance API for the picbackend app
"""


from django.test import TestCase
from django.test import Client
import json
import datetime
from .base_v2_api_tests import BaseV2APITests


class HealthInsuranceTradingPartnersAPITests(TestCase, BaseV2APITests):
    def setUp(self):
        self.base_url += "health_insurance_trading_partners/"


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class EligibilityValidPostTestBase(object):
    @classmethod
    def setUpClass(cls):
        cls.post_data = {"Birth Date": None,
                         "First Name": None,
                         "Last Name": None,
                         "Trading Partner ID": None,
                         "Gender": None,
                         "Consumer Plan ID": None}

    def test_for_ok_response_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_for_decoded_response_data(self):
        self.assertIsNotNone(self.response_data)

    def test_for_status_data(self):
        self.assertIsNotNone(self.status_data)

    def test_status_data_for_correct_version(self):
        self.assertEqual(self.status_data["Version"], 2.0)

    def test_status_data_for_valid_error_code(self):
        self.assertEqual(self.status_data["Error Code"], 0)

    def test_status_data_has_no_error_msgs(self):
        self.assertNotIn("Errors", self.status_data)

    def test_for_eligibility_data(self):
        self.assertIsNotNone(self.elig_data)

    def test_plan_start_date_in_eligibility_data(self):
        self.assertIn("Plan Start Date", self.elig_data)

    def test_plan_start_date_is_not_none(self):
        plan_start_date = self.elig_data["Plan Start Date"]

        self.assertIsNotNone(plan_start_date)

    def test_plan_start_date_is_string(self):
        plan_start_date = self.elig_data["Plan Start Date"]

        self.assertIsInstance(plan_start_date, str)

    def test_plan_start_date_is_valid_date(self):
        plan_start_date = self.elig_data["Plan Start Date"]

        self.assertTrue(validate_date(plan_start_date))

    def test_consumer_info_in_eligibility_data(self):
        self.assertIn("Consumer Info", self.elig_data)

    def test_consumer_info_is_dict(self):
        self.assertIsInstance(self.elig_data["Consumer Info"], dict)

    def test_plan_id_in_consumer_info(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIn("id", consumer_data)

    def test_plan_id_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIsInstance(consumer_data["id"], str)

    def test_birth_date_in_consumer_info(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIn("birth_date", consumer_data)

    def test_birth_date_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIsInstance(consumer_data["birth_date"], str)

    def test_birth_date_is_valid_date(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertTrue(validate_date(consumer_data["birth_date"]))

    def test_first_name_in_consumer_info(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIn("first_name", consumer_data)

    def test_first_name_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIsInstance(consumer_data["first_name"], str)

    def test_last_name_in_consumer_info(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIn("last_name", consumer_data)

    def test_last_name_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIsInstance(consumer_data["last_name"], str)

    def test_gender_in_consumer_info(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIn("gender", consumer_data)

    def test_gender_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIsInstance(consumer_data["gender"], str)

    def test_address_dict_in_consumer_info(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIn("address", consumer_data)

    def test_address_dict_is_dict(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIsInstance(consumer_data["address"], dict)

    def test_state_in_address_dict(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIn("state", address_data)

    def test_state_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIsInstance(address_data["state"], str)

    def test_zipcode_in_address_dict(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIn("zipcode", address_data)

    def test_zipcode_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIsInstance(address_data["zipcode"], str)

    def test_city_in_address_dict(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIn("city", address_data)

    def test_city_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIsInstance(address_data["city"], str)

    def test_address_lines_in_address_dict(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIn("address_lines", address_data)

    def test_address_lines_is_list(self):
        consumer_data = self.elig_data["Consumer Info"]
        address_data = consumer_data["address"]

        self.assertIsInstance(address_data["address_lines"], list)

    def test_payer_info_in_eligibility_data(self):
        self.assertIn("Payer Info", self.elig_data)

    def test_payer_info_is_dict(self):
        self.assertIsInstance(self.elig_data["Payer Info"], dict)

    def test_plan_id_in_payer_info(self):
        payer_data = self.elig_data["Payer Info"]

        self.assertIn("id", payer_data)

    def test_plan_id_in_payer_info_is_string(self):
        payer_data = self.elig_data["Payer Info"]

        self.assertIsInstance(payer_data["id"], str)

    def test_plan_name_in_payer_info(self):
        payer_data = self.elig_data["Payer Info"]

        self.assertIn("name", payer_data)

    def test_plan_name_in_payer_info_is_string(self):
        payer_data = self.elig_data["Payer Info"]

        self.assertIsInstance(payer_data["name"], str)

    def test_consumer_group_no_in_eligibility_data(self):
        self.assertIn("Consumer Group Number", self.elig_data)

    def test_consumer_group_no_is_string(self):
        self.assertIsInstance(self.elig_data["Consumer Group Number"], str)

    def test_service_types_in_eligibility_data(self):
        self.assertIn("Service Types", self.elig_data)

    def test_service_types_in_eligibility_data_is_list(self):
        self.assertIsInstance(self.elig_data["Service Types"], list)

    def test_service_types_in_eligibility_data_is_not_empty(self):
        service_types_list = self.elig_data["Service Types"]

        self.assertTrue(service_types_list)

    def test_coinsurance_benefits_in_eligibility_data(self):
        self.assertIn("Coinsurance Benefits", self.elig_data)

    def test_coinsurance_benefits_in_eligibility_data_is_list(self):
        self.assertIsInstance(self.elig_data["Coinsurance Benefits"], list)

    def test_coinsurance_benefits_in_eligibility_data_is_not_empty(self):
        coinsurance_benefits = self.elig_data["Coinsurance Benefits"]

        self.assertTrue(coinsurance_benefits)

    def test_elements_in_coinsurance_benefits_in_eligibility_data(self):
        coinsurance_benefits = self.elig_data["Coinsurance Benefits"]

        for elem in coinsurance_benefits:
            self.assertIn("coverage_level", elem)
            self.assertIsInstance(elem["coverage_level"], str)

            self.assertIn("service_type_codes", elem)
            self.assertIsInstance(elem["service_type_codes"], list)
            self.assertTrue(elem["service_type_codes"])

            self.assertIn("benefit_percent", elem)
            self.assertIsInstance(elem["benefit_percent"], float)

            self.assertIn("service_types", elem)
            self.assertIsInstance(elem["service_types"], list)
            self.assertTrue(elem["service_types"])

            self.assertIn("in_plan_network", elem)
            self.assertIsInstance(elem["in_plan_network"], str)
            self.assertIn(elem["in_plan_network"], ["yes", "no", "not_applicable"])

    def test_plan_description_in_eligibility_data(self):
        self.assertIn("Plan Description", self.elig_data)

    def test_plan_description_in_eligibility_data_is_string(self):
        self.assertIsInstance(self.elig_data["Plan Description"], str)

    def test_active_plan_in_eligibility_data(self):
        self.assertIn("Plan is Active", self.elig_data)

    def test_active_plan_in_eligibility_data_is_bool(self):
        self.assertIsInstance(self.elig_data["Plan is Active"], bool)

    def test_deductibles_in_eligibility_data(self):
        self.assertIn("Deductibles", self.elig_data)

    def test_deductibles_in_eligibility_data_is_dict(self):
        self.assertIsInstance(self.elig_data["Deductibles"], dict)

    def test_deductibles_in_eligibility_data_is_not_empty(self):
        deductibles_data = self.elig_data["Deductibles"]

        self.assertTrue(deductibles_data)

    def test_cal_year_data_in_deductibles_in_eligibility_data(self):
        deductibles_data = self.elig_data["Deductibles"]

        self.assertIn("Calendar Year Amounts", deductibles_data)

    def test_cal_year_data_in_deductibles_in_eligibility_data_is_list(self):
        deductibles_data = self.elig_data["Deductibles"]
        cal_year_list = deductibles_data["Calendar Year Amounts"]

        self.assertIsInstance(cal_year_list, list)

    def test_cal_year_data_in_deductibles_in_eligibility_data_is_not_empty(self):
        deductibles_data = self.elig_data["Deductibles"]
        cal_year_list = deductibles_data["Calendar Year Amounts"]

        self.assertTrue(cal_year_list)

    def test_elements_in_cal_year_data_in_deductibles_in_eligibility_data(self):
        deductibles_data = self.elig_data["Deductibles"]
        cal_year_list = deductibles_data["Calendar Year Amounts"]

        for elem in cal_year_list:
            self.assertIn("time_period", elem)
            self.assertIsInstance(elem["time_period"], str)
            self.assertEquals(elem["time_period"], "calendar_year")

            self.assertIn("service_types", elem)
            self.assertIsInstance(elem["service_types"], list)
            self.assertTrue(elem["service_types"])

            self.assertIn("in_plan_network", elem)
            self.assertIsInstance(elem["in_plan_network"], str)
            self.assertIn(elem["in_plan_network"], ["yes", "no", "not_applicable"])

            self.assertIn("coverage_level", elem)
            self.assertIsInstance(elem["coverage_level"], str)
            self.assertIn(elem["coverage_level"], ["family", "individual"])

            self.assertIn("service_type_codes", elem)
            self.assertIsInstance(elem["service_type_codes"], list)
            self.assertTrue(elem["service_type_codes"])

            benefit_amount_info = elem["benefit_amount"]
            self.assertIn("amount", benefit_amount_info)
            self.assertIsInstance(benefit_amount_info["amount"], str)
            self.assertIn("currency", benefit_amount_info)
            self.assertIsInstance(benefit_amount_info["currency"], str)

    def test_out_of_pocket_data_in_eligibility_data(self):
        self.assertIn("Out of Pocket", self.elig_data)

    def test_out_of_pocket_data_in_eligibility_data_is_dict(self):
        self.assertIsInstance(self.elig_data["Out of Pocket"], dict)

    def test_out_of_pocket_data_in_eligibility_data_is_not_empty(self):
        out_of_pocket_data = self.elig_data["Out of Pocket"]

        self.assertTrue(out_of_pocket_data)

    def test_cal_year_data_in_out_of_pocket_data_in_eligibility_data(self):
        out_of_pocket_data = self.elig_data["Out of Pocket"]

        self.assertIn("Calendar Year Amounts", out_of_pocket_data)

    def test_cal_year_data_in_out_of_pocket_data_in_eligibility_data_is_list(self):
        out_of_pocket_data = self.elig_data["Out of Pocket"]
        cal_year_list = out_of_pocket_data["Calendar Year Amounts"]

        self.assertIsInstance(cal_year_list, list)

    def test_cal_year_data_in_out_of_pocket_data_in_eligibility_data_is_not_empty(self):
        out_of_pocket_data = self.elig_data["Out of Pocket"]
        cal_year_list = out_of_pocket_data["Calendar Year Amounts"]

        self.assertTrue(cal_year_list)

    def test_elements_in_cal_year_data_in_out_of_pocket_data_in_eligibility_data(self):
        out_of_pocket_data = self.elig_data["Out of Pocket"]
        cal_year_list = out_of_pocket_data["Calendar Year Amounts"]

        for elem in cal_year_list:
            self.assertIn("time_period", elem)
            self.assertIsInstance(elem["time_period"], str)
            self.assertEquals(elem["time_period"], "calendar_year")

            self.assertIn("service_types", elem)
            self.assertIsInstance(elem["service_types"], list)
            self.assertTrue(elem["service_types"])

            self.assertIn("in_plan_network", elem)
            self.assertIsInstance(elem["in_plan_network"], str)
            self.assertIn(elem["in_plan_network"], ["yes", "no", "not_applicable"])

            self.assertIn("coverage_level", elem)
            self.assertIsInstance(elem["coverage_level"], str)
            self.assertIn(elem["coverage_level"], ["family", "individual"])

            self.assertIn("service_type_codes", elem)
            self.assertIsInstance(elem["service_type_codes"], list)
            self.assertTrue(elem["service_type_codes"])

            benefit_amount_info = elem["benefit_amount"]
            self.assertIn("amount", benefit_amount_info)
            self.assertIsInstance(benefit_amount_info["amount"], str)
            self.assertIn("currency", benefit_amount_info)
            self.assertIsInstance(benefit_amount_info["currency"], str)


class UnitedHealthcareTestsWithValidPost(TestCase, EligibilityValidPostTestBase):
    @classmethod
    def setUpClass(cls):
        TestCase.setUpClass()
        EligibilityValidPostTestBase.setUpClass()
        cls.post_data["Birth Date"] = "1989-05-01"
        cls.post_data["First Name"] = "Nicole"
        cls.post_data["Last Name"] = "Mahan"
        cls.post_data["Consumer Plan ID"] = None
        cls.post_data["Gender"] = None
        cls.post_data["Trading Partner ID"] = "united_health_care"
        json_post_data = json.dumps(cls.post_data)

        c = Client()
        cls.response = c.post('/v2/consumer_health_insurance_benefits/', json_post_data, content_type="application/json")

        response_data_json = cls.response.content.decode('utf-8')
        cls.response_data = json.loads(response_data_json)

        cls.status_data = cls.response_data["Status"]

        cls.elig_data = cls.response_data["Data"]

    def test_middle_name_in_consumer_info(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIn("middle_name", consumer_data)

    def test_middle_name_is_string(self):
        consumer_data = self.elig_data["Consumer Info"]

        self.assertIsInstance(consumer_data["middle_name"], str)

    def test_copay_info_in_eligibility_data(self):
        self.assertIn("Copay", self.elig_data)

    def test_copay_info_is_list(self):
        self.assertIsInstance(self.elig_data["Copay"], list)

    def test_copay_info_is_not_empty(self):
        copay_list = self.elig_data["Copay"]

        self.assertTrue(copay_list)

    def test_elements_in_copay_info(self):
        copay_list = self.elig_data["Copay"]

        for elem in copay_list:
            copayment_info = elem["copayment"]
            self.assertIn("amount", copayment_info)
            self.assertIsInstance(copayment_info["amount"], str)
            self.assertIn("currency", copayment_info)
            self.assertIsInstance(copayment_info["currency"], str)

            self.assertIn("service_type_codes", elem)
            self.assertIsInstance(elem["service_type_codes"], list)
            self.assertTrue(elem["service_type_codes"])

            self.assertIn("coverage_level", elem)
            self.assertIsInstance(elem["coverage_level"], str)

            self.assertIn("service_types", elem)
            self.assertIsInstance(elem["service_types"], list)
            self.assertTrue(elem["service_types"])

            self.assertIn("in_plan_network", elem)
            self.assertIsInstance(elem["in_plan_network"], str)
            self.assertIn(elem["in_plan_network"], ["yes", "no", "not_applicable"])

    def test_insurance_type_in_eligibility_data(self):
        self.assertIn("Insurance Type", self.elig_data)

    def test_insurance_type_is_string(self):
        self.assertIsInstance(self.elig_data["Insurance Type"], str)
