"""
This module defines the db Tables for storing data related to consumer patient stories.
"""

from django.db.models import Model
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.core.validators import MaxValueValidator

from ..general_concern_models import ConsumerGeneralConcern


class ConsumerSpecificConcern(Model):
    RESEARCH_WEIGHT_DEFAULT = 50

    question = CharField(max_length=10000, unique=True)
    related_general_concerns = ManyToManyField(
        ConsumerGeneralConcern,
        blank=True,
        related_name='related_specific_concerns'
    )
    research_weight = IntegerField(default=50, validators=[MaxValueValidator(100),])

    def return_values_dict(self):
        valuesdict = {"question": self.question,
                      "research_weight": self.research_weight,
                      "related_general_concerns": None,
                      "Database ID": self.id}

        related_gen_concerns_qset = self.related_general_concerns.all()
        if len(related_gen_concerns_qset):
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
