from django.contrib import admin
from picmodels.models import PICConsumer, Navigators, MetricsSubmission, PlanStat, Country, NavMetricsLocation, Address,\
    CredentialsModel, PICConsumerBackup, ConsumerCPSInfoEntry, CallToAction, HealthcareCarrier, HealthcarePlan,\
    HealthcareServiceCostEntry, HospitalWebTrafficData, ConsumerHospitalInfo, CaseManagementStatus,\
    CareAdvisorCustomer, ConsumerNote, ProviderLocation, ProviderNetwork, ConsumerSpecificConcern,\
    ConsumerGeneralConcern, HealthcareSubsidyEligibilityByFamSize, HealthcareServiceExpertise, MarketplaceAppointments
from presencescheduler.models import PICUser, Appointment, Location

# Register your models here.
admin.site.register(PICUser)
admin.site.register(Appointment)
admin.site.register(Location)
admin.site.register(PICConsumer)
admin.site.register(Navigators)
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
admin.site.register(CareAdvisorCustomer)
admin.site.register(ConsumerNote)
admin.site.register(ProviderNetwork)
admin.site.register(ProviderLocation)
admin.site.register(ConsumerGeneralConcern)
admin.site.register(ConsumerSpecificConcern)
admin.site.register(HealthcareSubsidyEligibilityByFamSize)
admin.site.register(HealthcareServiceExpertise)
admin.site.register(MarketplaceAppointments)
