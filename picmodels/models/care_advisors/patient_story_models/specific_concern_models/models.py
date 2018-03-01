"""
This module defines the db Tables for storing data related to consumer patient stories.
"""

from django.db.models import Model
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.core.validators import MaxValueValidator

from ..general_concern_models import ConsumerGeneralConcern

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_specific_concern_rows_with_given_question

from .services.read import retrieve_specific_concern_data_by_id
from .services.read import retrieve_specific_concern_data_by_question
from .services.read import retrieve_specific_concern_data_by_gen_concern_id
from .services.read import retrieve_specific_concern_data_by_gen_concern_id_subset
from .services.read import retrieve_specific_concern_data_by_gen_concern_name


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
        valuesdict = {
            "question": self.question,
            "research_weight": self.research_weight,
            "related_general_concerns": None,
            "Database ID": self.id
        }

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


ConsumerSpecificConcern.create_row_w_validated_params = classmethod(create_row_w_validated_params)
ConsumerSpecificConcern.update_row_w_validated_params = classmethod(update_row_w_validated_params)
ConsumerSpecificConcern.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
ConsumerSpecificConcern.check_for_specific_concern_rows_with_given_question = classmethod(check_for_specific_concern_rows_with_given_question)

ConsumerSpecificConcern.retrieve_specific_concern_data_by_id = classmethod(retrieve_specific_concern_data_by_id)
ConsumerSpecificConcern.retrieve_specific_concern_data_by_question = classmethod(retrieve_specific_concern_data_by_question)
ConsumerSpecificConcern.retrieve_specific_concern_data_by_gen_concern_id = classmethod(retrieve_specific_concern_data_by_gen_concern_id)
ConsumerSpecificConcern.retrieve_specific_concern_data_by_gen_concern_id_subset = classmethod(retrieve_specific_concern_data_by_gen_concern_id_subset)
ConsumerSpecificConcern.retrieve_specific_concern_data_by_gen_concern_name = classmethod(retrieve_specific_concern_data_by_gen_concern_name)
