from django.db import models

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import get_serialized_rows_by_id


class DefaultEnrollmentStepComplete(models.Model):
    consumer = models.ForeignKey('PICConsumer', on_delete=models.CASCADE)
    navigator = models.ForeignKey('Navigators', on_delete=models.CASCADE)
    cm_client = models.ForeignKey('CaseManagementClient', on_delete=models.CASCADE)
    cm_sequence = models.ForeignKey('CMSequences', on_delete=models.CASCADE)

    notes = models.TextField(blank=True, null=True)
    datetime_completed = models.DateTimeField(blank=True, null=True)
    client_appointment_datetime = models.DateTimeField(blank=True, null=True)

    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
        rest_url = 'default_enrollment_step_complete'

    def return_values_dict(self):
        values_dict = {
            "consumer": self.consumer.id if self.consumer else None,
            "navigator": self.navigator.id if self.navigator else None,
            "cm_client": self.cm_client.id if self.cm_client else None,
            "cm_sequence": self.cm_sequence.id if self.cm_sequence else None,

            "notes": self.notes,
            "datetime_completed": self.datetime_completed.isoformat() if self.datetime_completed else None,
            "client_appointment_datetime": self.client_appointment_datetime.isoformat() if self.client_appointment_datetime else None,

            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,

            "id": self.id
        }

        return values_dict
DefaultEnrollmentStepComplete.create_row_w_validated_params = classmethod(create_row_w_validated_params)
DefaultEnrollmentStepComplete.update_row_w_validated_params = classmethod(update_row_w_validated_params)
DefaultEnrollmentStepComplete.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
DefaultEnrollmentStepComplete.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
