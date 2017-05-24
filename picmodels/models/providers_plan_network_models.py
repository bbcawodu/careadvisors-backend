"""
This module defines the db Tables for storing provider networks and the plans that they accept.
"""

from django.db import models
from django.conf import settings
from django.dispatch import receiver


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
    sample_id_card = models.ImageField(upload_to='carrier_sample_id_cards/', default=settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)

    def check_state_choices(self,):
        if self.state_province:
            for state_tuple in self.STATE_CHOICES:
                if state_tuple[1].lower() == self.state_province.lower():
                    return True
            return False
        else:
            return True

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "state": None,
                      "plans": None,
                      "sample_id_card": self.sample_id_card.url,
                      "Database ID": self.id}

        # add related plans to values dict
        member_plans = []
        for plan_object in self.healthcareplan_set.all():
            member_plans.append(plan_object.id)

        if member_plans:
            valuesdict["plans"] = member_plans

        if self.state_province:
            valuesdict['state'] = self.state_province

        return valuesdict


@receiver(models.signals.post_delete, sender=HealthcareCarrier)
def remove_file_from_s3(sender, instance, using, **kwargs):
    default_sample_id_card_url = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)
    if instance.sample_id_card.url != default_sample_id_card_url:
        instance.sample_id_card.delete(save=False)


class HealthcarePlan(models.Model):
    HMO = "HMO"
    PPO = "PPO"
    POS = 'POS'
    EPO = 'EPO'
    N_A = "Not Available"
    PREMIUM_CHOICES = ((HMO, "HMO"),
                       (PPO, "PPO"),
                       (POS, 'POS'),
                       (EPO, 'EPO'),
                       (N_A, "Not Available")
                       )

    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = 'Platinum'
    CATASTROPHIC = "Catastrophic"
    METAL_CHOICES = ((BRONZE, "Bronze"),
                     (SILVER, "Silver"),
                     (GOLD, "Gold"),
                     (PLATINUM, 'Platinum'),
                     (CATASTROPHIC, "Catastrophic"),
                     (N_A, "Not Available"))

    name = models.CharField(max_length=10000)
    carrier = models.ForeignKey(HealthcareCarrier, on_delete=models.CASCADE, blank=True, null=True)
    premium_type = models.CharField(max_length=1000, blank=True, null=True, choices=PREMIUM_CHOICES)
    metal_level = models.CharField(max_length=1000, blank=True, null=True, choices=METAL_CHOICES)

    def check_metal_choices(self,):
        if self.metal_level:
            for metal_tuple in self.METAL_CHOICES:
                if metal_tuple[1].lower() == self.metal_level.lower():
                    return True
            return False
        else:
            return True

    def check_premium_choices(self,):
        if self.premium_type:
            for premium_tuple in self.PREMIUM_CHOICES:
                if premium_tuple[1].lower() == self.premium_type.lower():
                    return True
            return False
        else:
            return True

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "premium_type": self.premium_type,
                      "metal_level": self.metal_level,
                      "carrier_info": None,
                      "Database ID": self.id}

        if self.carrier:
            carrier_info = {"name": self.carrier.name,
                            "state": self.carrier.state_province,
                            "Database ID": self.carrier.id}
            valuesdict['carrier_info'] = carrier_info

        return valuesdict


class ProviderNetwork(models.Model):
    name = models.CharField(max_length=10000)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "provider_locations": None,
                      "Database ID": self.id}

        # add related plans to values dict
        provider_locations = []
        for provider_location in self.providerlocation_set.all():
            provider_locations.append(provider_location.id)

        if provider_locations:
            valuesdict["provider_locations"] = provider_locations

        return valuesdict


class ProviderLocation(models.Model):
    name = models.CharField(max_length=10000)
    accepted_plans = models.ManyToManyField(HealthcarePlan, blank=True, related_name='locations_accepted_at')
    provider_network = models.ForeignKey(ProviderNetwork, on_delete=models.CASCADE, blank=True, null=True)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "provider_network info": None,
                      "accepted_plans": None,
                      "Database ID": self.id}

        if self.provider_network:
            provider_network_object = self.provider_network
            provider_network_info = {
                                        "name": provider_network_object.name,
                                        "Database ID": provider_network_object.id
                                    }
            valuesdict['provider_network info'] = provider_network_info

        accepted_plans_queryset = self.accepted_plans.all()
        if accepted_plans_queryset.count():
            accepted_plans_ids = []
            for plan_object in accepted_plans_queryset:
                accepted_plans_ids.append(plan_object.id)
            valuesdict['accepted_plans'] = accepted_plans_ids

        return valuesdict
