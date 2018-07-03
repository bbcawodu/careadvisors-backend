import copy

from django.test import TestCase

from picmodels.tests.models.base import DBModelsBaseTestCase

from picmodels.models import CMSequences


class CMSequencesTestCase(DBModelsBaseTestCase, TestCase):
    db_model = CMSequences
    validated_params = {
        "name": "shitstain",

        "db_action": "create",
    }

    def test_create_row_w_validated_params(self):
        validated_params = copy.deepcopy(self.validated_params)
        validated_params["add_steps"] = [3]
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

    def test_create_row_w_validated_params_w_errors(self):
        validated_params = copy.deepcopy(self.validated_params)
        del validated_params['name']
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

    def test_update_row_w_validated_params(self):
        validated_params = copy.deepcopy(self.validated_params)
        validated_params["db_action"] = "update"
        validated_params["add_steps"] = [3]
        validated_params["id"] = 4

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

        validated_params = copy.deepcopy(self.validated_params)
        validated_params["db_action"] = "update"
        validated_params["name"] = "update"
        validated_params["remove_steps"] = [3]
        validated_params["id"] = 1

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

    def test_update_row_w_validated_params_w_errors(self):
        validated_params = {
            "db_action":  "update",
        }
        test_errors = []

        db_row = self.use_update_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

        validated_params = {
            "db_action": "update",
            "id": 1,
            "add_steps": [4]
        }
        test_errors = []

        db_row = self.use_update_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

        validated_params = {
            "db_action": "update",
            "id": 4,
            "add_steps": [9]
        }
        test_errors = []

        db_row = self.use_update_row_w_validated_params_w_errors(
            validated_params,
            test_errors
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

    def test_delete_row_w_validated_params_w_errors(self):
        validated_params = {
            "db_action": "delete"
        }
        test_errors = []

        self.use_delete_row_w_validated_params_w_errors(
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
        self.assertEqual(len(serialized_table_data), 1, "{}".format(serialized_table_data))

    def test_get_serialized_rows_by_name(self):
        validated_params = {
            "name": u"Health Risk Assessment"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_name(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 1, "{}".format(serialized_table_data))
