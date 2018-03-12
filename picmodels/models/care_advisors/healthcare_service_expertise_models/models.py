from django.db.models import Model
from django.db.models import CharField

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_rows_with_rqst_name

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_name


class HealthcareServiceExpertise(Model):
    name = CharField(max_length=1000, unique=True)

    def return_values_dict(self):
        values_dict = {
            "name": self.name,
            "id": self.id
        }

        return values_dict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


HealthcareServiceExpertise.create_row_w_validated_params = classmethod(create_row_w_validated_params)
HealthcareServiceExpertise.update_row_w_validated_params = classmethod(update_row_w_validated_params)
HealthcareServiceExpertise.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
HealthcareServiceExpertise.check_for_rows_with_rqst_name = classmethod(check_for_rows_with_rqst_name)

HealthcareServiceExpertise.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
HealthcareServiceExpertise.get_serialized_rows_by_name = classmethod(get_serialized_rows_by_name)
