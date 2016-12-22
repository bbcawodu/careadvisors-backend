from django.test import TestCase
from django.core import management


class BaseWithDBTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
        # management.call_command('loaddata', '12-21-2016.json', verbosity=0)