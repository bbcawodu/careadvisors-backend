from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import MarketplaceAppointments


class MarketplaceAppointmentsTestCase(DBModelsBaseTestCase, TestCase):
    db_model = MarketplaceAppointments

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

    def test_get_serialized_rows_by_nav_id(self):
        validated_params = {
            "nav_id_list": [1],
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_nav_id(
            validated_params,
            test_errors
        )
