import datetime
import pytz
import copy

from django.test import TestCase

from picmodels.tests.models.base import DBModelsBaseTestCase

from picmodels.models import ContactLog


class ContactLogTestCase(DBModelsBaseTestCase, TestCase):
    db_model = ContactLog
    validated_params = {
        "consumer_id": 1,
        "navigator_id": 1,
        "cm_client_id": 1,

        "status": "completed",
        "contact_type": "email",
        "notes": "asihfiasuhw",
        "datetime_contacted": datetime.datetime.strptime("2018-06-22T17:00:00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC),
        "outcome": "wqoisaajfisajk",

        "db_action": "create",
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
                db_row.consumer.id,
                validated_params['consumer_id'],
                "row consumer id: {}, request consumer id: {}".format(db_row.consumer.id, validated_params['consumer_id'])
            )

    def test_create_row_w_validated_params_errors(self):
        validated_params = copy.deepcopy(self.validated_params)
        validated_params['status'] = 'shit_myself'
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

        validated_params = copy.deepcopy(self.validated_params)
        del validated_params['consumer_id']
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

        validated_params = copy.deepcopy(self.validated_params)
        del validated_params['status']
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

        validated_params = copy.deepcopy(self.validated_params)
        del validated_params['contact_type']
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

    def test_update_row_w_validated_params(self):
        validated_params = copy.deepcopy(self.validated_params)
        validated_params["db_action"] = "update"
        validated_params["id"] = 9

        test_errors = []

        db_row = self.use_update_row_w_validated_params(
            validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.consumer.id,
                validated_params['consumer_id'],
                "row consumer id: {}, request consumer id: {}".format(db_row.consumer.id, validated_params['consumer_id'])
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
            "id": 4,
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

        validated_params = {
            "id": u"all",
            "consumer_id_list": [
                4
            ],
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 7, "{}".format(serialized_table_data))

        validated_params["consumer_id_list"] = [
            2
        ]
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 1, "{}".format(serialized_table_data))

        validated_params["consumer_id_list"] = [
            1
        ]
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 4, "{}".format(serialized_table_data))

        validated_params["consumer_id_list"] = [
            1,
            2,
            4
        ]
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 12, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "nav_id_list": [
                1
            ],
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 10, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "cm_client_id": "1",
            "cm_client_id_list": [
                1
            ],
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 4, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "status": "completed",
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 10, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "contact_type": "email",
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 7, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "date_created_start": datetime.datetime.strptime("2018-05-30", "%Y-%m-%d").replace(tzinfo=pytz.UTC),
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 11, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "date_created_end": datetime.datetime.strptime("2018-5-29T23:59:59", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC),
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 1, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "date_modified_start": datetime.datetime.strptime("2018-05-30", "%Y-%m-%d").replace(tzinfo=pytz.UTC),
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 11, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "date_modified_end": datetime.datetime.strptime("2018-5-29T23:59:59", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC),
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 1, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "datetime_contacted_start_date": datetime.datetime.strptime("2018-5-30", "%Y-%m-%d").replace(tzinfo=pytz.UTC),
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 11, "{}".format(serialized_table_data))

        validated_params = {
            "id": u"all",
            "datetime_contacted_end_date": datetime.datetime.strptime("2018-5-29T23:59:59", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC),
        }
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )
        self.assertEqual(len(serialized_table_data), 1, "{}".format(serialized_table_data))
