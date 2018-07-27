from django.db import models

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import get_serialized_rows_by_id


class ContactLog(models.Model):
    N_A = "not available"
    OPEN = "Open"
    VOICE_MESSAGE = "Voice Message"
    COMPLETED = "Completed"
    PENDING = "Pending"
    WCB = "WCB"
    BT = "BT"
    NS = "NS"
    WN = "WN"
    STATUS_CHOICES = (
        (OPEN, "Open"),
        (VOICE_MESSAGE, "Voice Message"),
        (COMPLETED, "Completed"),
        (PENDING, "Pending"),
        (WCB, "WCB"),
        (BT, "BT"),
        (NS, "NS"),
        (WN, "WN"),
        (N_A, "not available")
    )

    EMAIL = "Email"
    TEXT = "Text"
    PHONE = "Phone"
    IN_PERSON = "In-Person"
    MAIL = "Mail"
    HOME_VISIT = "Home Visit"
    ON_SITE = "On Site"
    CONTACT_TYPE_CHOICES = (
        (EMAIL, "Email"),
        (TEXT, "Text"),
        (PHONE, "Phone"),
        (IN_PERSON, "In-Person"),
        (MAIL, "Mail"),
        (HOME_VISIT, "Home Visit"),
        (ON_SITE, "On Site"),
        (N_A, "not available")
    )

    consumer = models.ForeignKey('PICConsumer', on_delete=models.CASCADE)
    navigator = models.ForeignKey('Navigators', on_delete=models.CASCADE)
    cm_client = models.ForeignKey('CaseManagementClient', on_delete=models.CASCADE, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    outcome = models.CharField(max_length=5000, blank=True, null=True)
    status = models.CharField(max_length=1000, blank=True, null=True, choices=STATUS_CHOICES, default=N_A)
    datetime_contacted = models.DateTimeField(blank=True, null=True)
    contact_type = models.CharField(max_length=1000, blank=True, null=True, choices=CONTACT_TYPE_CHOICES, default=N_A)

    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    def check_status_choices(self,):
        for status_tuple in self.STATUS_CHOICES:
            if status_tuple[1].lower() == self.status.lower():
                return True
        return False

    def check_contact_type_choices(self,):
        for contact_type_tuple in self.CONTACT_TYPE_CHOICES:
            if contact_type_tuple[1].lower() == self.contact_type.lower():
                return True
        return False

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

    def return_values_dict(self):
        values_dict = {
            "consumer": self.consumer.id if self.consumer else None,
            "navigator": self.navigator.id if self.navigator else None,
            "cm_client": self.cm_client.id if self.cm_client else None,

            "notes": self.notes,
            "outcome": self.outcome,
            "status": self.status,
            "datetime_contacted": self.datetime_contacted.isoformat() if self.datetime_contacted else None,
            "contact_type": self.contact_type,

            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,

            "id": self.id
        }

        return values_dict
ContactLog.create_row_w_validated_params = classmethod(create_row_w_validated_params)
ContactLog.update_row_w_validated_params = classmethod(update_row_w_validated_params)
ContactLog.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
ContactLog.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
