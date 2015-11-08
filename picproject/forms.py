"""
This file contains form classes for abstracting
forms across 
"""
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from picmodels.models import PICUser


YES_NO_CHOICE = [
    ('', 'Please Choose'),
    (0, 'No'),
    (1, 'Yes'),
]

class UserCreateForm(UserCreationForm):
	password = forms.CharField(max_length=30, required=False)
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	email = forms.EmailField(required=True)
	address = forms.CharField(max_length=1000, required=True)
	phone_number = forms.CharField(max_length=1000, required=True)

	class Meta:
		model = User
		fields = '__all__'

	def save(self, commit=True):
		if not commit:
			raise NotImplementedError("Can't create User and UserProfile without database save")
		user = super(UserCreateForm, self).save(commit=True)
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.email = self.cleaned_data["email"]
		pic_user_profile = PICUser(user=user, address=self.cleaned_data['address'], phone_number=self.cleaned_data['phone_number'])
		pic_user_profile.save()
		return user, pic_user_profile


class AssessmentFormOne(forms.Form):
	has_heartdisease = forms.ChoiceField(choices=YES_NO_CHOICE)
	has_mentalillness = forms.ChoiceField(choices=YES_NO_CHOICE)
	has_disability = forms.ChoiceField(choices=YES_NO_CHOICE)
	has_obesity = forms.ChoiceField(choices=YES_NO_CHOICE)
	does_smoke = forms.ChoiceField(choices=YES_NO_CHOICE)
	is_employed = forms.ChoiceField(choices=YES_NO_CHOICE)
	has_insurance = forms.ChoiceField(choices=YES_NO_CHOICE)
	has_primary_doctor = forms.ChoiceField(choices=YES_NO_CHOICE)
	
	
    # subject = forms.CharField()
    # email = forms.EmailField(required=False)
    # message = forms.CharField()

class AssessmentFormTwo(forms.Form):

	def __init__(self, previous_form_data, *args, **kwargs):
		super(AssessmentFormTwo, self).__init__(*args, **kwargs)

		if previous_form_data['has_heartdisease'] == 1:
			self.fields['heartdisease_over_10'] = forms.ChoiceField(choices=YES_NO_CHOICE)
		else:
			self.fields['has_history_of_heartdisease'] = forms.ChoiceField(choices=YES_NO_CHOICE)

		if previous_form_data['has_mentalillness'] == 1:
			self.fields['mental_illness_over_1'] = forms.ChoiceField(choices=YES_NO_CHOICE)
		else:
			self.fields['has_history_of_mentalillness'] = forms.ChoiceField(choices=YES_NO_CHOICE)

		if previous_form_data['does_smoke'] == 1:
			self.fields['smoke_atleast_a_pack_a_day'] = forms.ChoiceField(choices=YES_NO_CHOICE)