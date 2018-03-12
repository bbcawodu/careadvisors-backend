from django.db import models
from picmodels.models.care_advisors import PICConsumer
from picmodels.models.care_advisors import Navigators

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_nav_id


class MarketplaceAppointments(models.Model):
    # fields for appointment model
    consumer = models.ForeignKey(PICConsumer, on_delete=models.SET_NULL, blank=True, null=True)
    navigator = models.ForeignKey(Navigators, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def return_values_dict(self):
        values_dict = {
            "date": self.date.isoformat() if self.date else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "navigator_id": self.navigator_id if self.navigator else None,
            "consumer_id": self.consumer_id if self.consumer else None,
            "id": self.id
        }

        return values_dict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


MarketplaceAppointments.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
MarketplaceAppointments.get_serialized_rows_by_nav_id = classmethod(get_serialized_rows_by_nav_id)
