import datetime

from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import PICConsumer
from picmodels.models import Navigators


class PICConsumerTestCase(DBModelsBaseTestCase, TestCase):
    db_model = PICConsumer

    def test_create_row_w_validated_params(self):
        validated_params = {
            "first_name": "Hitsugaya",
            "middle_name": "",
            "last_name": "Toshiro",
            "email": "ksf@lis.com",
            "phone": "2813307004",
            "met_nav_at": "Sullivan High School",
            "household_size": 7,
            "plan": "Medicaid",
            "best_contact_time": "",
            "preferred_language": "English",
            "consumer_notes": [
                # "",
                #  "ksjdh"
            ],
            "address_line_1": "",
            "address_line_2": "",
            "city": "",
            "state_province": "",
            "zipcode": "",

            "date_met_nav": datetime.date(2018, 5, 3),

            "navigator_row": Navigators.objects.get(id=1),

            "validated_cps_info_dict": None,
            "validated_hospital_info_dict": None,

            'billing_amount': 1000.0,
            'consumer_need': 'choose a doctor',
            'service_expertise_need': 'bariatrics',
            'insurance_carrier': {
                'name': 'Health Alliance Medical Plans, Inc.',
                'state_province': 'il'
            },
            'add_healthcare_locations_used': [
                {
                    'name': 'Edward Hospital & Immediate Careasdss',
                    'state_province': 'not available'
                }
            ],

            "db_action": "create",
            "create_backup": True,
            "force_create_consumer": True,
        }
        test_errors = []

        matching_db_rows, db_row, backup_db_row = self.use_create_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.first_name,
                validated_params['first_name'],
                "row name: {}, request name: {}".format(db_row.first_name, validated_params['first_name'])
            )

    def test_update_row_w_validated_params(self):
        validated_params = {
            "first_name": "Zaraki",
            "middle_name": "",
            "last_name": "Kenpachi",
            "email": "ksf@lis.com",
            "phone": "2813307004",
            "met_nav_at": "Sullivan High School",
            "household_size": 7,
            "plan": "Medicaid",
            "preferred_language": "English",
            "consumer_notes": [
                # "",
                #  "ksjdh"
            ],
            "address_line_1": "",
            "address_line_2": "",
            "city": "",
            "state_province": "",
            "zipcode": "",

            "date_met_nav": datetime.date(2018, 5, 3),

            "navigator_row": Navigators.objects.get(id=1),

            'billing_amount': 1000.0,
            'consumer_need': 'choose a doctor',
            'service_expertise_need': 'bariatrics',
            'insurance_carrier': {
                'name': 'Health Alliance Medical Plans, Inc.',
                'state_province': 'il'
            },
            'remove_healthcare_locations_used': [
                {
                    'name': 'Edward Hospital & Immediate Careasdss',
                    'state_province': 'not available'
                }
            ],

            "db_action": "update",
            "id": 312,
            # "create_backup": True,
            # "force_create_consumer": True,
        }
        test_errors = []

        db_row, backup_db_row = self.use_update_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.first_name,
                validated_params['first_name'],
                "row name: {}, request name: {}".format(db_row.first_name, validated_params['first_name'])
            )

    def test_delete_row_w_validated_params(self):
        validated_params = {
            "id": 4,
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

    def test_get_serialized_rows_by_first_name(self):
        validated_params = {
            "first_name_list": ['bradley'],
            "first_name": u"bradley"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_first_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_last_name(self):
        validated_params = {
            "last_name_list": ['awodu'],
            "last_name": u"awodu"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_last_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_f_and_l_name(self):
        validated_params = {
            "first_name_list": ['bradley'],
            "first_name": u"bradley",
            "last_name_list": ['awodu'],
            "last_name": u"awodu"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_f_and_l_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_email(self):
        validated_params = {
            "email_list": ['jermaine@piccares.org'],
            "email": u"jermaine@piccares.org"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_email(
            validated_params,
            test_errors
        )
