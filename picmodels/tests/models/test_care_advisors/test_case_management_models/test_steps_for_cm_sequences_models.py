import copy
from django.test import TestCase

from picmodels.tests.models.base import DBModelsBaseTestCase

from picmodels.models import StepsForCMSequences


class StepsForCMSequencesTestCase(DBModelsBaseTestCase, TestCase):
    db_model = StepsForCMSequences
    validated_params = {
        "step_name": "Test Enrollment Step",
        "step_class_name": "TestEnrollmentStep",
        "step_number": 3,

        "db_action": "create"
    }

    def test_create_row_w_validated_params(self):
        validated_params = copy.deepcopy(self.validated_params)
        test_errors = []

        db_row = self.use_create_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.step_name,
                validated_params['step_name'],
                "row step_name: {}, request step_name: {}".format(db_row.step_name, validated_params['step_name'])
            )

            self.assertEqual(
                db_row.rest_url,
                'test_enrollment_step',
                db_row.rest_url
            )

    def test_create_row_w_validated_params_w_errors(self):
        validated_params = copy.deepcopy(self.validated_params)
        del validated_params['step_class_name']
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

        validated_params = copy.deepcopy(self.validated_params)
        del validated_params['step_name']
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

    def test_update_row_w_validated_params(self):
        validated_params = copy.deepcopy(self.validated_params)
        validated_params["db_action"] = "update"
        validated_params["id"] = 3
        test_errors = []

        db_row = self.use_update_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.step_name,
                validated_params['step_name'],
                "row step_name: {}, request step_name: {}".format(db_row.step_name, validated_params['step_name'])
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
            "id": u"all"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 4)

        validated_params = {
            "id_list": [3],
            "id": u"3"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 1)

    def test_get_serialized_rows_by_name(self):
        validated_params = {
            "name": u"default enrollment step 1"
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_name(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 1)
