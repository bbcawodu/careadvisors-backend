"""
Defines tests for version 1 of the navigator hub locations API for the picbackend app
"""


from django.test import TestCase
from .base_v1_api_tests import BaseV1APITests


class NavHubLocationAPITests(TestCase, BaseV1APITests):
    def setUp(self):
        self.base_url += "navlocations/"
