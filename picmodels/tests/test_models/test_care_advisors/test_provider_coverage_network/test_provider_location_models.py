from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import ProviderLocation
from picmodels.models import HealthcarePlan


class ProviderLocationTestCase(DBModelsBaseTestCase, TestCase):
    db_model = ProviderLocation

    def test_create_row_w_validated_params(self):
        validated_params = {
            "name": "Neonatal",
            'state_province': 'il',
            "provider_network_id": 1,

            "add_accepted_plans_objects": [
                HealthcarePlan.objects.get(id=8778)
            ],

            "db_action": "create"
        }
        test_errors = []

        db_row = self.use_create_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.name,
                validated_params['name'],
                "row name: {}, request name: {}".format(db_row.name, validated_params['name'])
            )

    def test_update_row_w_validated_params(self):
        validated_params = {
            "name": "Neonatalss",
            'state_province': 'il',
            "provider_network_id": 1,

            "add_accepted_plans_objects": [
                HealthcarePlan.objects.get(id=8778)
            ],
            # "remove_accepted_plans_objects": [
            #     HealthcarePlan.objects.get(id=8778)
            # ],

            "id": 3,
            "db_action": "update"
        }
        test_errors = []

        db_row = self.use_update_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.name,
                validated_params['name'],
                "row name: {}, request name: {}".format(db_row.name, validated_params['name'])
            )

    def test_delete_row_w_validated_params(self):
        validated_params = {
            "id": 3,
            "db_action": "delete"
        }
        test_errors = []

        self.use_delete_row_w_validated_params(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_id(self):
        validated_params = {
            "id_list": [3],
            "id": u"3"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_name(self):
        validated_params = {
            "name": "Edward Hospital & Immediate Care"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_network_id(self):
        validated_params = {
            "network_id_list": [1],
            "network_id": u"1"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_network_id(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_network_name(self):
        validated_params = {
            "network_name": "Edward-Elmhurst"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_network_name(
            validated_params,
            test_errors
        )
