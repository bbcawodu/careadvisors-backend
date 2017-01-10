"""
Defines tests for version 1 of the consumer metrics API for the picbackend app
"""


from django.test import TestCase
from .base_v1_api_tests import BaseConsumerStaffMetricsTests


class ConsumerMetricsAPITests(TestCase, BaseConsumerStaffMetricsTests):
    def setUp(self):
        self.base_url += "metrics/"
