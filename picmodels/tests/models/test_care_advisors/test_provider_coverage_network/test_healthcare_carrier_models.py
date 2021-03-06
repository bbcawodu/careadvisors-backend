from django.test import TestCase

from picmodels.tests.models.base import DBModelsBaseTestCase

from picmodels.models import HealthcareCarrier


class HealthcareCarrierTestCase(DBModelsBaseTestCase, TestCase):
    db_model = HealthcareCarrier

    def test_create_row_w_validated_params(self):
        validated_params = {
            "name": "Neonatal",
            "state": "il",

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
            "state": "il",

            "id": 6097,
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
            "id": 6095,
            "db_action": "delete"
        }
        test_errors = []

        self.use_delete_row_w_validated_params(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_id(self):
        validated_params = {
            "id_list": [6097],
            "id": u"6097"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_name(self):
        validated_params = {
            "name" : "Premera Blue Cross Blue Shield of Alaska"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_name(
            validated_params,
            test_errors
        )
