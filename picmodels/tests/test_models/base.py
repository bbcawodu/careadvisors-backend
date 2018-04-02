from django.test import Client
from django.conf import settings


class DBModelsBaseTestCase(object):
    client_object = Client(content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    settings.DEBUG = True

    def use_create_row_w_validated_params(self, validated_params, rqst_errors):
        db_row = self.db_model.create_row_w_validated_params(
            validated_params,
            rqst_errors
        )

        self.assertEqual(len(rqst_errors), 0, "{}".format(rqst_errors))
        self.assertNotEqual(db_row, None, "{}".format(db_row))

        return db_row

    def use_update_row_w_validated_params(self, validated_params, rqst_errors):
        db_row = self.db_model.update_row_w_validated_params(
            validated_params,
            rqst_errors
        )

        self.assertEqual(len(rqst_errors), 0, "{}".format(rqst_errors))
        self.assertNotEqual(db_row, None, "{}".format(db_row))

        return db_row

    def use_delete_row_w_validated_params(self, validated_params, rqst_errors):
        self.db_model.delete_row_w_validated_params(
            validated_params,
            rqst_errors
        )

        self.assertEqual(len(rqst_errors), 0, "{}".format(rqst_errors))

    def use_get_serialized_rows_by_id(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_id(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_name(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_name(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_nav_id(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_nav_id(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_network_name(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_network_name(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_network_id(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_network_id(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_first_name(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_first_name(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_last_name(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_last_name(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_f_and_l_name(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_f_and_l_name(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_email(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_email(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_county(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_county(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_region(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_region(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_mpn(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_mpn(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_company_name(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_company_name(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data

    def use_get_serialized_rows_by_phone_number(self, validated_params, test_errors):
        serialized_table_data = self.db_model.get_serialized_rows_by_phone_number(
            validated_params,
            test_errors
        )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(serialized_table_data), 0, "{}".format([serialized_table_data]))

        return serialized_table_data
