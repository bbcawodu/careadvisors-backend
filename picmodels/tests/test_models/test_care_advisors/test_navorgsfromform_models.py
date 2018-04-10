import datetime
import pytz

from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import NavOrgsFromOnlineForm


class NavOrgsFromOnlineFormTestCase(DBModelsBaseTestCase, TestCase):
    db_model = NavOrgsFromOnlineForm

    def test_create_row_w_validated_params(self):
        validated_params = {
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

            "appointment_datetime": datetime.datetime.strptime("2018-05-03T17:00:00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC),


            "db_action": "create",
        }
        test_errors = []

        db_row = self.use_create_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.company_name,
                validated_params['company_name'],
                "row name: {}, request name: {}".format(db_row.company_name, validated_params['company_name'])
            )

    def test_update_row_w_validated_params(self):
        validated_params = {
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

            "appointment_datetime": datetime.datetime.strptime("2018-05-03T17:00:00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC),
            "appointment_datetime_2": datetime.datetime.strptime("2018-05-04T17:00:00", "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=pytz.UTC),
            "appointment_datetime_3": datetime.datetime.strptime("2018-05-05T17:00:00", "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=pytz.UTC),

            "db_action": "update",
            "id": 1,
        }
        test_errors = []

        db_row = self.use_update_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.company_name,
                validated_params['company_name'],
                "row company_name: {}, request company_name: {}".format(db_row.company_name, validated_params['company_name'])
            )

            self.assertEqual(
                db_row.appointment_datetime_2,
                validated_params['appointment_datetime_2'],
                "row appointment_datetime_2: {}, request appointment_datetime_2: {}".format(db_row.appointment_datetime_2,
                                                                        validated_params['appointment_datetime_2'])
            )

            self.assertEqual(
                db_row.appointment_datetime_3,
                validated_params['appointment_datetime_3'],
                "row appointment_datetime_3: {}, request appointment_datetime_3: {}".format(db_row.appointment_datetime_3,
                                                                        validated_params['appointment_datetime_3'])
            )

    def test_delete_row_w_validated_params(self):
        validated_params = {
            "id": 2,
            "db_action": "delete"
        }
        test_errors = []

        self.use_delete_row_w_validated_params(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_id(self):
        validated_params = {
            "id_list": [1],
            "id": u"1"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_email(self):
        validated_params = {
            "email_list": ['applemartini@gmail.com'],
            "email": u"applemartini@gmail.com"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_email(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_company_name(self):
        validated_params = {
            "company_name_list": ["Shithole Enterprises"],
            "company_name": u"Shithole Enterprises"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_company_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_phone_number(self):
        validated_params = {
            "phone_number_list": ['2813307004'],
            "phone_number": u"2813307004"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_phone_number(
            validated_params,
            test_errors
        )
