from django.db import models
from django.core.validators import MinValueValidator

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_name


class StepsForCMSequences(models.Model):
    step_name = models.CharField(max_length=500, unique=True)
    step_table_name = models.CharField(max_length=500, unique=True)
    step_class_name = models.CharField(max_length=500, unique=True)
    step_number = models.IntegerField(validators=[MinValueValidator(0), ])

    class Meta:
        app_label = 'picmodels'
        verbose_name_plural = "Steps for Case Management Sequences"

    def return_values_dict(self):
        values_dict = {
            "step_name": self.step_name,
            "step_table_name": self.step_table_name,
            "step_class_name": self.step_class_name,
            "step_number": self.step_number,

            "id": self.id,
        }

        return values_dict
StepsForCMSequences.create_row_w_validated_params = classmethod(create_row_w_validated_params)
StepsForCMSequences.update_row_w_validated_params = classmethod(update_row_w_validated_params)
StepsForCMSequences.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
StepsForCMSequences.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
StepsForCMSequences.get_serialized_rows_by_name = classmethod(get_serialized_rows_by_name)
