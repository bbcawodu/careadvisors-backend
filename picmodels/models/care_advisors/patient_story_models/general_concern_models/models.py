"""
This module defines the db Tables for storing data related to consumer patient stories.
"""

from django.db.models import Model
from django.db.models import CharField
from operator import itemgetter

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_general_concern_objs_with_given_name

from .services.read import retrieve_general_concerns_by_id
from .services.read import retrieve_general_concerns_by_name
from .services.read import retrieve_related_gen_concern_rows_by_name


class ConsumerGeneralConcern(Model):
    name = CharField(max_length=1000, unique=True)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "related_specific_concerns": None,
                      "Database ID": self.id}

        related_specific_concerns_qset = self.related_specific_concerns.all()
        if len(related_specific_concerns_qset):
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


ConsumerGeneralConcern.create_row_w_validated_params = classmethod(create_row_w_validated_params)
ConsumerGeneralConcern.update_row_w_validated_params = classmethod(update_row_w_validated_params)
ConsumerGeneralConcern.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
ConsumerGeneralConcern.check_for_general_concern_objs_with_given_name = classmethod(check_for_general_concern_objs_with_given_name)

ConsumerGeneralConcern.retrieve_general_concerns_by_id = classmethod(retrieve_general_concerns_by_id)
ConsumerGeneralConcern.retrieve_general_concerns_by_name = classmethod(retrieve_general_concerns_by_name)
ConsumerGeneralConcern.retrieve_related_gen_concern_rows_by_name = classmethod(retrieve_related_gen_concern_rows_by_name)
