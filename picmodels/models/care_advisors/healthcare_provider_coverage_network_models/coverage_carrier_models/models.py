from django.db import models
from django.conf import settings
from django.dispatch import receiver
import uuid
import os
import urllib

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_healthcare_carrier_objs_with_given_name_and_state

from .services.read import retrieve_carrier_data_by_id
from .services.read import retrieve_carrier_data_by_name
from .services.read import retrieve_carrier_data_by_state


def get_sample_id_card_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('carrier_sample_id_cards', filename)


class HealthcareCarrier(models.Model):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"

    STATE_CHOICES = ((AL, "AL"),
                     (AK, "AK"),
                     (AZ, "AZ"),
                     (AR, "AR"),
                     (CA, "CA"),
                     (CO, "CO"),
                     (CT, "CT"),
                     (DE, "DE"),
                     (FL, "FL"),
                     (GA, "GA"),
                     (HI, "HI"),
                     (ID, "ID"),
                     (IL, "IL"),
                     (IN, "IN"),
                     (IA, "IA"),
                     (KS, "KS"),
                     (KY, "KY"),
                     (LA, "LA"),
                     (ME, "ME"),
                     (MD, "MD"),
                     (MA, "MA"),
                     (MI, "MI"),
                     (MN, "MN"),
                     (MS, "MS"),
                     (MO, "MO"),
                     (MT, "MT"),
                     (NE, "NE"),
                     (NV, "NV"),
                     (NH, "NH"),
                     (NJ, "NJ"),
                     (NM, "NM"),
                     (NY, "NY"),
                     (NC, "NC"),
                     (ND, "ND"),
                     (OH, "OH"),
                     (OK, "OK"),
                     (OR, "OR"),
                     (PA, "PA"),
                     (RI, "RI"),
                     (SC, "SC"),
                     (SD, "SD"),
                     (TN, "TN"),
                     (TX, "TX"),
                     (UT, "UT"),
                     (VT, "VT"),
                     (VA, "VA"),
                     (WA, "WA"),
                     (WV, "WV"),
                     (WI, "WI"),
                     (WY, "WY")
                     )

    name = models.CharField(max_length=10000)
    state_province = models.CharField("State/Province", max_length=40, blank=True, null=True, choices=STATE_CHOICES)
    sample_id_card = models.ImageField(upload_to=get_sample_id_card_file_path, blank=True, null=True)

    def check_state_choices(self,):
        if self.state_province:
            for state_tuple in self.STATE_CHOICES:
                if state_tuple[1].lower() == self.state_province.lower():
                    return True
            return False
        else:
            return True

    def return_values_dict(self):
        valuesdict = {
            "name": self.name,
            "url_encoded_name": urllib.parse.quote(self.name) if self.name else None,
            "state": None,
            "plans": None,
            "sample_id_card": None,
            "Database ID": self.id
        }

        # add related plans to values dict
        member_plans = []
        if self.healthcareplan_set:
            carrier_plan_qset = self.healthcareplan_set.all()
            if len(carrier_plan_qset):
                for plan_object in carrier_plan_qset:
                    member_plans.append(plan_object.id)
        if member_plans:
            valuesdict["plans"] = member_plans

        if self.state_province:
            valuesdict['state'] = self.state_province

        if self.sample_id_card:
            valuesdict["sample_id_card"] = self.sample_id_card.url
        else:
            valuesdict["sample_id_card"] = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


HealthcareCarrier.create_row_w_validated_params = classmethod(create_row_w_validated_params)
HealthcareCarrier.update_row_w_validated_params = classmethod(update_row_w_validated_params)
HealthcareCarrier.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
HealthcareCarrier.check_for_healthcare_carrier_objs_with_given_name_and_state = classmethod(check_for_healthcare_carrier_objs_with_given_name_and_state)

HealthcareCarrier.retrieve_carrier_data_by_id = classmethod(retrieve_carrier_data_by_id)
HealthcareCarrier.retrieve_carrier_data_by_name = classmethod(retrieve_carrier_data_by_name)
HealthcareCarrier.retrieve_carrier_data_by_state = classmethod(retrieve_carrier_data_by_state)


@receiver(models.signals.post_delete, sender=HealthcareCarrier)
def remove_file_from_s3(sender, instance, using, **kwargs):
    default_sample_id_card_url = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)

    if instance.sample_id_card:
        if instance.sample_id_card.url != default_sample_id_card_url:
            instance.sample_id_card.delete(save=False)
