"""
Defines tests for version 2 of the navigator hub locations API for the picbackend app
"""


from django.test import TestCase
from .base_v2_api_tests import BaseV2APITests


class NavHubLocationAPITests(TestCase, BaseV2APITests):
    def setUp(self):
        self.base_url += "navigator_hub_locations/"
