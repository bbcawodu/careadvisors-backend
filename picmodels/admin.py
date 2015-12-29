from django.contrib import admin
from picmodels.models import PICUser, Appointment, Location, PICConsumer, PICStaff, MetricsSubmission

# Register your models here.
admin.site.register(PICUser)
admin.site.register(Appointment)
admin.site.register(Location)
admin.site.register(PICConsumer)
admin.site.register(PICStaff)
admin.site.register(MetricsSubmission)