from django.db import models

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_rows_with_given_name

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_name


class CMSequences(models.Model):
    name = models.CharField(max_length=200, unique=True)
    steps = models.ManyToManyField("StepsForCMSequences", blank=True, null=True)

    class Meta:
        app_label = 'picmodels'
        verbose_name_plural = "Case Management Sequences"

    def return_values_dict(self):
        values_dict = {
            "name": self.name,
            "steps": None,
            "id": self.id,
        }

        sequence_steps = self.steps.all()
        if len(sequence_steps):
            sequence_step_values = []
            for step in sequence_steps:
                sequence_step_values.append(step.return_values_dict())
            values_dict["steps"] = sequence_step_values

        return values_dict
CMSequences.create_row_w_validated_params = classmethod(create_row_w_validated_params)
CMSequences.update_row_w_validated_params = classmethod(update_row_w_validated_params)
CMSequences.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
CMSequences.check_for_rows_with_given_name = classmethod(check_for_rows_with_given_name)
CMSequences.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
CMSequences.get_serialized_rows_by_name = classmethod(get_serialized_rows_by_name)
