from django.test import TestCase
from django.core import management


class BaseWithDBTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        management.call_command('loaddata', '12-13-2016.json', verbosity=0)