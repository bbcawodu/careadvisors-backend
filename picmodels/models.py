"""
This file defines the data models for the picproject app
"""

from django.db import models, IntegrityError
from django.contrib.auth.models import User
import datetime


# Create your models here.
class PICUser(models.Model):
    # one to one reference to django built in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional fields for PICUser model
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=1000)

    # maps model to the picmodels module
    class Meta:
        app_label = 'picmodels'


class PICConsumer(models.Model):
    # fields for PICConsumer model
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=1000)
    preferred_language = models.CharField(max_length=1000)
    best_contact_time = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

        unique_together = ("first_name",
                           "last_name",
                           "email",
                           "phone",
                           "preferred_language",
                           "best_contact_time")


class Location(models.Model):
    # fields for Location model
    name = models.CharField(max_length=1000)
    address = models.CharField(max_length=2000)
    phone = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class PICStaff(models.Model):
    # fields for PICStaff model
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=1000)
    county = models.CharField(blank=True, max_length=1000, default="")

    def return_values_dict(self):
        valuesdict = {"First Name": self.first_name,
                      "Last Name": self.last_name,
                      "Email": self.email,
                      "Type": self.type,
                      "Database ID": self.id,
                      "County": self.county}
        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class Appointment(models.Model):
    # fields for appointment model
    consumer = models.ForeignKey(PICConsumer, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    poc = models.ForeignKey(PICStaff, on_delete=models.CASCADE, blank=True, null=True)
    date = models.CharField(max_length=2000)
    start_time = models.CharField(max_length=1000)
    end_time = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class PlanStat(models.Model):
    ALL_SAVERS = "All Savers Insurance Company"
    CARESOURCE_INDIANA = "CareSource Indiana, Inc."
    HUMANA_HEALTH = "Humana Health Plan, Inc."
    H_A_M_P = "Health Alliance Medical Plans, Inc."
    BLUE_CROSS_BLUES_SHIELD = "Blue Cross Blue Shield of Illinois"
    COVENTRY_HEALTH_IL = "Coventry Health Care of Illinois, Inc."
    COVENTRY = "Coventry Health & Life Co."
    UNITED_HEALTHCARE_MIDWEST = "United Healthcare of the Midwest, Inc."
    CELTIC_INSURANCE = "Celtic Insurance Company"
    HARKEN_HEALTH = "Harken Health Insurance Company"
    AETNA = "Aetna Health Inc."
    SE_IN_HEALTH_ORG = "Southeastern Indiana Health Organization"
    ANTHEM = "Anthem Ins Companies Inc(Anthem BCBS)"
    PHYSICIANS_HEALTH_N_IN = "Physicians Health Plan of Northern Indiana, Inc."
    MDWISE_MARKETPLACE = "MDwise Marketplace, Inc."
    IU_HEALTH_PLANS = "Indiana University Health Plans, Inc."
    MISCELLANEOUS = "Miscellaneous"
    PLAN_CHOICES = ((ALL_SAVERS, "All Savers Insurance Company"),
                    (CARESOURCE_INDIANA, "CareSource Indiana, Inc."),
                    (HUMANA_HEALTH, "Humana Health Plan, Inc."),
                    (H_A_M_P, "Health Alliance Medical Plans, Inc."),
                    (BLUE_CROSS_BLUES_SHIELD, "Blue Cross Blue Shield of Illinois"),
                    (COVENTRY_HEALTH_IL, "Coventry Health Care of Illinois, Inc."),
                    (COVENTRY, "Coventry Health & Life Co."),
                    (UNITED_HEALTHCARE_MIDWEST, "United Healthcare of the Midwest, Inc."),
                    (CELTIC_INSURANCE, "Celtic Insurance Company"),
                    (HARKEN_HEALTH, "Harken Health Insurance Company"),
                    (AETNA, "Aetna Health Inc."),
                    (SE_IN_HEALTH_ORG, "Southeastern Indiana Health Organization"),
                    (ANTHEM, "Anthem Ins Companies Inc(Anthem BCBS)"),
                    (PHYSICIANS_HEALTH_N_IN, "Physicians Health Plan of Northern Indiana, Inc."),
                    (MDWISE_MARKETPLACE, "MDwise Marketplace, Inc."),
                    (IU_HEALTH_PLANS, "Indiana University Health Plans, Inc."),
                    (MISCELLANEOUS, "Miscellaneous"))

    HMO = "HMO"
    PPO = "PPO"
    N_A = "Not Available"
    PREMIUM_CHOICES = ((HMO, "HMO"),
                       (PPO, "PPO"),
                       (N_A, "Not Available"))

    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    CATASTROPHIC = "Catastrophic"
    METAL_CHOICES = ((BRONZE, "Bronze"),
                     (SILVER, "Silver"),
                     (GOLD, "Gold"),
                     (CATASTROPHIC, "Catastrophic"),
                     (N_A, "Not Available"))

    plan_name = models.CharField(max_length=1000,
                                 choices=PLAN_CHOICES,
                                 default=MISCELLANEOUS)
    premium_type = models.CharField(max_length=1000, blank=True, choices=PREMIUM_CHOICES, default=N_A)
    metal_level = models.CharField(max_length=1000, blank=True, choices=METAL_CHOICES, default=N_A)
    enrollments = models.IntegerField()

    def check_plan_choices(self,):
        for plan_tuple in self.PLAN_CHOICES:
            if plan_tuple[1].lower() == self.plan_name.lower():
                return True
        return False

    def check_premium_choices(self,):
        for premium_tuple in self.PREMIUM_CHOICES:
            if premium_tuple[1].lower() == self.premium_type.lower():
                return True
        return False

    def check_metal_choices(self,):
        for metal_tuple in self.METAL_CHOICES:
            if metal_tuple[1].lower() == self.metal_level.lower():
                return True
        return False

    def save(self, *args, **kwargs):
        super(PlanStat, self).save(*args, **kwargs)


class MetricsSubmission(models.Model):
    # fields for PICStaff model
    staff_member = models.ForeignKey(PICStaff, on_delete=models.CASCADE)
    plan_stats = models.ManyToManyField(PlanStat)
    received_education = models.IntegerField()
    applied_medicaid = models.IntegerField()
    selected_qhp = models.IntegerField()
    enrolled_shop = models.IntegerField()
    ref_medicaid_or_chip = models.IntegerField()
    ref_shop = models.IntegerField()
    filed_exemptions = models.IntegerField()
    rec_postenroll_support = models.IntegerField()
    trends = models.CharField(max_length=5000, blank=True, default="")
    success_story = models.CharField(max_length=5000)
    hardship_or_difficulty = models.CharField(max_length=5000)
    comments = models.CharField(max_length=5000, blank=True, default="")
    outreach_stakeholder_activity = models.CharField(max_length=5000, blank=True, default="")
    appointments_scheduled = models.IntegerField(blank=True, null=True)
    confirmation_calls = models.IntegerField(blank=True, null=True)
    appointments_held = models.IntegerField(blank=True, null=True)
    appointments_over_hour = models.IntegerField(blank=True, null=True)
    appointments_cmplx_market = models.IntegerField(blank=True, null=True)
    appointments_cmplx_medicaid = models.IntegerField(blank=True, null=True)
    appointments_postenroll_assistance = models.IntegerField(blank=True, null=True)
    appointments_over_three_hours = models.IntegerField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    county = models.CharField(max_length=1000, default="")
    zipcode = models.CharField(max_length=1000, default="")
    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)

    def return_values_dict(self):
        valuesdict = {"Received Education": self.received_education,
                      "Applied Medicaid": self.applied_medicaid,
                      "Selected QHP": self.selected_qhp,
                      "Enrolled SHOP": self.enrolled_shop,
                      "Referred Medicaid or CHIP": self.ref_medicaid_or_chip,
                      "Referred SHOP": self.ref_shop,
                      "Filed Exemptions": self.filed_exemptions,
                      "Received Post-Enrollment Support": self.rec_postenroll_support,
                      "Trends": self.trends,
                      "Success Story": self.success_story,
                      "Hardship or Difficulty": self.hardship_or_difficulty,
                      "Comments": self.comments,
                      "Outreach and Stakeholder Activities": self.outreach_stakeholder_activity,
                      "Appointments Scheduled": self.appointments_scheduled,
                      "Confirmation Calls": self.confirmation_calls,
                      "Appointments Held": self.appointments_held,
                      "Appointments Over Hour": self.appointments_over_hour,
                      "Appointments Complex Market": self.appointments_cmplx_market,
                      "Appointments Complex Medicaid": self.appointments_cmplx_medicaid,
                      "Appointments Post-Enrollment Assistance": self.appointments_postenroll_assistance,
                      "Appointments Over 3 Hours": self.appointments_over_three_hours,
                      "Staff Member ID": self.staff_member_id,
                      "Date Created": self.date_created.isoformat(),
                      "Submission Date": self.submission_date.isoformat(),
                      "County": self.county,
                      "Zipcode": self.zipcode,
                      "Plan Stats": [],
                      }
        plan_stats = self.plan_stats.all()
        if len(plan_stats) > 0:
            for plan_stat_object in plan_stats:
                plan_stat_dict = {"Issuer Name": plan_stat_object.plan_name,
                                  "Enrollments": plan_stat_object.enrollments,
                                  "Metal Level": plan_stat_object.metal_level,
                                  "Premium Type": plan_stat_object.premium_type}
                valuesdict["Plan Stats"].append(plan_stat_dict)

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'