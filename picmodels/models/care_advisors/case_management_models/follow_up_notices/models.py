from django.db import models

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import get_serialized_rows_by_id


class FollowUpNotices(models.Model):
    N_A = "not available"
    OPEN = "Open"
    COMPLETED = "Completed"
    STATUS_CHOICES = (
        (OPEN, "Open"),
        (COMPLETED, "Completed"),
        (N_A, "not available")
    )

    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "HIGH"
    URGENT = "Urgent"
    SEVERITY_CHOICES = (
        (LOW, "Low"),
        (NORMAL, "Normal"),
        (HIGH, "HIGH"),
        (URGENT, "Urgent"),
        (N_A, "not available")
    )

    consumer = models.ForeignKey('PICConsumer', on_delete=models.CASCADE)
    navigator = models.ForeignKey('Navigators', on_delete=models.CASCADE)

    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1000, blank=True, null=True, choices=STATUS_CHOICES, default=N_A)
    severity = models.CharField(max_length=1000, blank=True, null=True, choices=SEVERITY_CHOICES, default=N_A)

    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    def check_status_choices(self,):
        for status_tuple in self.STATUS_CHOICES:
            if status_tuple[1].lower() == self.status.lower():
                return True
        return False

    def check_severity_choices(self,):
        for severity_tuple in self.SEVERITY_CHOICES:
            if severity_tuple[1].lower() == self.severity.lower():
                return True
        return False

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

    def return_values_dict(self):
        values_dict = {
            "consumer": self.consumer.id if self.consumer else None,
            "navigator": self.navigator.id if self.navigator else None,

            "notes": self.notes,
            "status": self.status,
            "severity": self.severity,

            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,

            "id": self.id
        }

        return values_dict
FollowUpNotices.create_row_w_validated_params = classmethod(create_row_w_validated_params)
FollowUpNotices.update_row_w_validated_params = classmethod(update_row_w_validated_params)
FollowUpNotices.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
FollowUpNotices.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
