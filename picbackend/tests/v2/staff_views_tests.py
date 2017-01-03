"""
Defines tests for version 2 of the staff API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseConsumerStaffMetricsTests


class StaffAPITests(TestCase, BaseConsumerStaffMetricsTests):
    def setUp(self):
        self.base_url += "staff/"
