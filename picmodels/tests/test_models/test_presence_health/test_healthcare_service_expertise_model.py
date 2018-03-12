from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import HealthcareServiceExpertise


class HealthcareServiceExpertiseTestCase(DBModelsBaseTestCase, TestCase):
    db_model = HealthcareServiceExpertise

    def test_create_row_w_validated_params(self):
        validated_params = {
            "name": "Neonatal",

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

            "id": 1,
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
            "id": 1,
            "db_action": "delete"
        }
        test_errors = []

        self.use_delete_row_w_validated_params(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_id(self):
        session_ids_to_get = [
            1
        ]
        session_ids_to_get_string = u"1"
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            session_ids_to_get_string,
            session_ids_to_get,
            test_errors
        )

    def test_get_serialized_rows_by_name(self):
        session_name_to_get = u"cancer"
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_name(
            session_name_to_get,
            test_errors
        )
