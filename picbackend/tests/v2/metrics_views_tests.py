"""
Defines tests for version 2 of the consumer metrics API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseConsumerStaffMetricsTests


class ConsumerMetricsAPITests(TestCase, BaseConsumerStaffMetricsTests):
    def setUp(self):
        self.base_url += "metrics/"
