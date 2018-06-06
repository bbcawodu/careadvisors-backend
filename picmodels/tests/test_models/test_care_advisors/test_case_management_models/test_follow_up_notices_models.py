import copy

from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import FollowUpNotices


class FollowUpNoticesTestCase(DBModelsBaseTestCase, TestCase):
    db_model = FollowUpNotices
    validated_params = {
        "consumer_id": 1,
        "navigator_id": 1,

        "status": "completed",
        "severity": "high",
        "notes": "asihfiasuhw",

        "db_action": "create",
    }

    def test_create_row_w_validated_params(self):
        test_errors = []

        db_row = self.use_create_row_w_validated_params(
            self.validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.consumer.id,
                self.validated_params['consumer_id'],
                "row consumer id: {}, request consumer id: {}".format(db_row.consumer.id, self.validated_params['consumer_id'])
            )

    def test_create_row_w_validated_params_errors(self):
        validated_params = copy.deepcopy(self.validated_params)
        validated_params['status'] = 'shit_myself'
        test_errors = []

        db_row = self.use_create_row_w_validated_params_w_errors(
            validated_params,
            test_errors
        )

    def test_update_row_w_validated_params(self):
        # self.validated_params["first_name"] = "Hitsugayasdasa"
        # self.validated_params["last_name"] = "Toshiro"
        # self.validated_params["email"] = "ksf@lis.com"
        # self.validated_params["type"] = "Navigator"
        # self.validated_params["county"] = 'Cook'
        # self.validated_params["mpn"] = "12984892137"
        #
        # self.validated_params["address_line_1"] = ""
        # self.validated_params["address_line_2"] = ""
        # self.validated_params["city"] = ""
        # self.validated_params["state_province"] = ""
        # self.validated_params["zipcode"] = ""
        #
        # self.validated_params["phone"] = "2813307004"
        # self.validated_params["reported_region"] = "cook"
        # self.validated_params["video_link"] = "https://www.twitch.tv/videos/239858398"
        #
        self.validated_params["db_action"] = "update"
        self.validated_params["id"] = 5

        test_errors = []

        db_row = self.use_update_row_w_validated_params(
            self.validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.consumer.id,
                self.validated_params['consumer_id'],
                "row consumer id: {}, request consumer id: {}".format(db_row.consumer.id, self.validated_params['consumer_id'])
            )

    def test_delete_row_w_validated_params(self):
        self.validated_params["id"] = 4
        self.validated_params["db_action"] = "delete"

        test_errors = []

        self.use_delete_row_w_validated_params(
            self.validated_params,
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
