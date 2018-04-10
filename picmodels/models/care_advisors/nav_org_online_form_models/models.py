from django.db import models
from django.core.validators import MinValueValidator
import urllib

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

#
from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_email
from .services.read import get_serialized_rows_by_company_name
from .services.read import get_serialized_rows_by_phone_number


class NavOrgsFromOnlineForm(models.Model):
    company_name = models.CharField(max_length=1000, blank=True, null=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    estimated_monthly_caseload = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    contact_first_name = models.CharField(max_length=500, blank=True, null=True)
    contact_last_name = models.CharField(max_length=500, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=500, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    appointment_datetime = models.DateTimeField(blank=True, null=True)
    appointment_datetime_2 = models.DateTimeField(blank=True, null=True)
    appointment_datetime_3 = models.DateTimeField(blank=True, null=True)

    def return_values_dict(self):
        values_dict = {
            "company_name": self.company_name,
            "url_encoded_company_name": urllib.parse.quote(self.company_name) if self.company_name else None,
            "address": None,
            "estimated_monthly_caseload": self.estimated_monthly_caseload,
            "contact_first_name": self.contact_first_name,
            "contact_last_name": self.contact_last_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "date_created": self.date_created.isoformat() if self.date_created else None,
            "appointment_datetime": self.appointment_datetime.isoformat() if self.appointment_datetime else None,
            "appointment_datetime_2": self.appointment_datetime_2.isoformat() if self.appointment_datetime_2 else None,
            "appointment_datetime_3": self.appointment_datetime_3.isoformat() if self.appointment_datetime_3 else None,

            "id": self.id
        }

        if self.address:
            values_dict["address"] = {}
            address_values = self.address.return_values_dict()
            for key in address_values:
                values_dict["address"][key] = address_values[key]

        return values_dict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


NavOrgsFromOnlineForm.create_row_w_validated_params = classmethod(create_row_w_validated_params)
NavOrgsFromOnlineForm.update_row_w_validated_params = classmethod(update_row_w_validated_params)
NavOrgsFromOnlineForm.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)

NavOrgsFromOnlineForm.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
NavOrgsFromOnlineForm.get_serialized_rows_by_email = classmethod(get_serialized_rows_by_email)
NavOrgsFromOnlineForm.get_serialized_rows_by_company_name = classmethod(get_serialized_rows_by_company_name)
NavOrgsFromOnlineForm.get_serialized_rows_by_phone_number = classmethod(get_serialized_rows_by_phone_number)
