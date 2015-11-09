"""
This file defines the data models for the picproject app
"""



from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PICUser(models.Model):
	#one to one reference to django built in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #additional fields for PICUser model
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=1000)

    #maps model to the picmodels module
    class Meta:
    	app_label = 'picmodels'