from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import MarketplaceAppointments


class HealthcareServiceExpertiseTestCase(DBModelsBaseTestCase, TestCase):
    db_model = MarketplaceAppointments

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

    def test_get_serialized_rows_by_nav_id(self):
        nav_ids_to_get = [
            1
        ]
        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_nav_id(
            nav_ids_to_get,
            test_errors
        )
