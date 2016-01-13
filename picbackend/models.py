from django.db import models
from django.contrib.auth.models import User


class PICUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=1000)

    class Meta:
        app_label = 'picbackend'
