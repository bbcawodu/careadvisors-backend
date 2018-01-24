from django.contrib import admin
from picmodels.models import PICUser, Appointment, Location, PICConsumer, PICStaff, MetricsSubmission, PlanStat,\
    Country, NavMetricsLocation, Address, CredentialsModel, PICConsumerBackup, ConsumerCPSInfoEntry, CallToAction,\
    HealthcareCarrier, HealthcarePlan, HealthcareServiceCostEntry, HospitalWebTrafficData, ConsumerHospitalInfo,\
    CaseManagementStatus

# Register your models here.
admin.site.register(PICUser)
admin.site.register(Appointment)
admin.site.register(Location)
admin.site.register(PICConsumer)
admin.site.register(PICStaff)
admin.site.register(MetricsSubmission)
admin.site.register(PlanStat)
admin.site.register(Country)
admin.site.register(NavMetricsLocation)
admin.site.register(Address)
admin.site.register(CredentialsModel)
admin.site.register(PICConsumerBackup)
admin.site.register(ConsumerCPSInfoEntry)
admin.site.register(CallToAction)
admin.site.register(HealthcareCarrier)
admin.site.register(HealthcarePlan)
admin.site.register(HealthcareServiceCostEntry)
admin.site.register(HospitalWebTrafficData)
admin.site.register(ConsumerHospitalInfo)
admin.site.register(CaseManagementStatus)
