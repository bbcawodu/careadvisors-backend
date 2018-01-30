"""
This file defines the data models for Hospital Web Traffic Data
"""

from django.db import models
from math import ceil

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_traffic_rows_w_name

from .services.read import retrieve_hospital_traffic_data_by_id
from .services.read import retrieve_hospital_traffic_data_by_name


class HospitalWebTrafficData(models.Model):
    PERCENTAGE_OF_MONTHLY_VISITS_SEEKING_HEALTH_SERVICES = .092
    PERCENTAGE_OF_MONTHLY_VISITS_WHO_SPILL_OFF = .0598

    hospital_name = models.CharField(max_length=10000)
    monthly_visits = models.IntegerField(blank=True, null=True)

    @property
    def consumers_seeking_health_services(self):
        if self.monthly_visits:
            return ceil(self.PERCENTAGE_OF_MONTHLY_VISITS_SEEKING_HEALTH_SERVICES * self.monthly_visits)
        else:
            return None

    @property
    def consumers_who_spill_off(self):
        if self.monthly_visits:
            return ceil(self.PERCENTAGE_OF_MONTHLY_VISITS_WHO_SPILL_OFF * self.monthly_visits)
        else:
            return None

    def return_values_dict(self):
        values_dict = {
            "hospital_name": self.hospital_name,
            "monthly_visits": self.monthly_visits,
            "consumers_seeking_health_services": self.consumers_seeking_health_services,
            "consumers_who_spill_off": self.consumers_who_spill_off,
            "Database ID": self.id
        }

        return values_dict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


HospitalWebTrafficData.create_row_w_validated_params = classmethod(create_row_w_validated_params)
HospitalWebTrafficData.update_row_w_validated_params = classmethod(update_row_w_validated_params)
HospitalWebTrafficData.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
HospitalWebTrafficData.check_for_traffic_rows_w_name = classmethod(check_for_traffic_rows_w_name)

HospitalWebTrafficData.retrieve_hospital_traffic_data_by_id = classmethod(retrieve_hospital_traffic_data_by_id)
HospitalWebTrafficData.retrieve_hospital_traffic_data_by_name = classmethod(retrieve_hospital_traffic_data_by_name)
