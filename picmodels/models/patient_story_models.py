"""
This module defines the db Tables for storing data related to consumer patient stories.
"""

from django.db.models import Model
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.core.validators import MaxValueValidator
from operator import itemgetter


class ConsumerGeneralConcern(Model):
    name = CharField(max_length=1000, unique=True)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "related_specific_concerns": None,
                      "Database ID": self.id}

        related_specific_concerns_qset = self.related_specific_concerns.all()
        if related_specific_concerns_qset.count():
            specific_concerns_list = []
            for specific_concern_object in related_specific_concerns_qset:
                specific_concern_dict = {
                    "question": specific_concern_object.question,
                    "research_weight": specific_concern_object.research_weight,
                    "Database ID": specific_concern_object.id
                }
                specific_concerns_list.append(specific_concern_dict)

            sorted_specific_concerns_list = sorted(specific_concerns_list, key=itemgetter('research_weight'), reverse=True)
            valuesdict["related_specific_concerns"] = sorted_specific_concerns_list

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class ConsumerSpecificConcern(Model):
    question = CharField(max_length=10000, unique=True)
    related_general_concerns = ManyToManyField(ConsumerGeneralConcern, blank=True, related_name='related_specific_concerns')
    research_weight = IntegerField(default=50, validators=[MaxValueValidator(100),])

    def return_values_dict(self):
        valuesdict = {"question": self.question,
                      "research_weight": self.research_weight,
                      "related_general_concerns": None,
                      "Database ID": self.id}

        related_gen_concerns_qset = self.related_general_concerns.all()
        if related_gen_concerns_qset.count():
            general_concerns_list = []
            for gen_concern_object in related_gen_concerns_qset:
                gen_concern_dict = {
                    "name": gen_concern_object.name,
                    "Database ID": gen_concern_object.id
                }
                general_concerns_list.append(gen_concern_dict)
            valuesdict["related_general_concerns"] = general_concerns_list

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
