from django.db import models

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import get_serialized_rows_by_id


class DefaultEnrollmentStep1(models.Model):
    N_A = "Not Available"
    ACTIVE = "Active"
    IN_PROGRESS_WITH_BENEFITS_ORG = "In progress with benefits org"
    ON_HOLD = "On hold"
    CLOSED = "Closed"
    CASE_STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (IN_PROGRESS_WITH_BENEFITS_ORG, "In progress with benefits org"),
        (ON_HOLD, "On hold"),
        (CLOSED, "Closed"),
        (N_A, "Not Available")
    )

    consumer = models.ForeignKey('PICConsumer', on_delete=models.CASCADE)
    navigator = models.ForeignKey('Navigators', on_delete=models.CASCADE)
    cm_client = models.ForeignKey('CaseManagementClient', on_delete=models.CASCADE)
    cm_sequence = models.ForeignKey('CMSequences', on_delete=models.CASCADE)

    notes = models.TextField(blank=True, null=True)
    tracking_no = models.CharField(max_length=500, blank=True, null=True)
    user_name = models.CharField(max_length=500, blank=True, null=True)
    datetime_completed = models.DateTimeField(blank=True, null=True)

    primary_care_physician = models.CharField(max_length=500, blank=True, null=True)
    appointment_datetime = models.DateTimeField(blank=True, null=True)
    policy_number = models.CharField(max_length=500, blank=True, null=True)
    resource_case_number = models.CharField(max_length=500, blank=True, null=True)
    expedite_benefits_organization_contact_name = models.CharField(max_length=500, blank=True, null=True)
    expedite_benefits_organization_contact_phone = models.CharField(max_length=500, blank=True, null=True)
    customer_service_success = models.CharField(max_length=500, blank=True, null=True)
    case_status = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        choices=CASE_STATUS_CHOICES,
        default=N_A
    )

    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
        rest_url = 'default_enrollment_step_1'

    def check_case_status_choices(self,):
        for case_status_tuple in self.CASE_STATUS_CHOICES:
            if case_status_tuple[1].lower() == self.case_status.lower():
                return True
        return False

    def return_values_dict(self):
        values_dict = {
            "consumer": self.consumer.id if self.consumer else None,
            "navigator": self.navigator.id if self.navigator else None,
            "cm_client": self.cm_client.id if self.cm_client else None,
            "cm_sequence": self.cm_sequence.id if self.cm_sequence else None,

            "notes": self.notes,
            "tracking_no": self.tracking_no,
            "user_name": self.user_name,
            "datetime_completed": self.datetime_completed.isoformat() if self.datetime_completed else None,

            "primary_care_physician": self.primary_care_physician,
            "appointment_datetime": self.appointment_datetime.isoformat() if self.appointment_datetime else None,
            "policy_number": self.policy_number,
            "resource_case_number": self.resource_case_number,
            "expedite_benefits_organization_contact_name": self.expedite_benefits_organization_contact_name,
            "expedite_benefits_organization_contact_phone": self.expedite_benefits_organization_contact_phone,
            "customer_service_success": self.customer_service_success,
            "case_status": self.case_status,

            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,

            "id": self.id
        }

        return values_dict
DefaultEnrollmentStep1.create_row_w_validated_params = classmethod(create_row_w_validated_params)
DefaultEnrollmentStep1.update_row_w_validated_params = classmethod(update_row_w_validated_params)
DefaultEnrollmentStep1.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
DefaultEnrollmentStep1.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
