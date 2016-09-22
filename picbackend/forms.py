"""
This file contains form classes for abstracting
forms across 
"""

from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from picmodels.models import PICUser, NavMetricsLocation, Country

# defines dictionary mapping choices to values for forms.ChoiceField
YES_NO_CHOICE = [
    ('', 'Please Choose'),
    (0, 'No'),
    (1, 'Yes'),
]


class NavMetricsLocationForm(ModelForm):
    # country = ModelChoiceField(queryset=Country.objects.all(), empty_label="Choose Country", to_field_name="name")

    def __init__(self, *args, **kwargs):
        super(NavMetricsLocationForm, self).__init__(*args, **kwargs)
        self.fields['country'].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = NavMetricsLocation
        fields = ["name", "address_line1", "address_line2", "zipcode", "city", "state_province", "country"]


# defines form class for creating user registration form
class UserCreateForm(UserCreationForm):
    password = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=30, required=True, error_messages={'required': 'Please enter first name.'})
    last_name = forms.CharField(max_length=30, required=True, error_messages={'required': 'Please enter last name.'})
    email = forms.EmailField(required=True, error_messages={'required': 'Please enter email.'})
    address = forms.CharField(max_length=1000, required=True, error_messages={'required': 'Please enter address.'})
    phone_number = forms.CharField(max_length=1000, required=True,
                                   error_messages={'required': 'Please enter phone number.'})

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
        pic_user_profile = PICUser(user=user, address=self.cleaned_data['address'],
                                   phone_number=self.cleaned_data['phone_number'])
        pic_user_profile.save()
        return user, pic_user_profile


# defines form class for creating part 1 of risk assessment form
class AssessmentFormOne(forms.Form):
    has_heartdisease = forms.ChoiceField(choices=YES_NO_CHOICE,
                                         error_messages={'required': 'Please answer heart disease question.'})
    has_mentalillness = forms.ChoiceField(choices=YES_NO_CHOICE,
                                          error_messages={'required': 'Please answer mental illness question.'})
    has_disability = forms.ChoiceField(choices=YES_NO_CHOICE,
                                       error_messages={'required': 'Please answer disability question.'})
    has_obesity = forms.ChoiceField(choices=YES_NO_CHOICE,
                                    error_messages={'required': 'Please answer obesity question.'})
    does_smoke = forms.ChoiceField(choices=YES_NO_CHOICE,
                                   error_messages={'required': 'Please answer smoking question.'})
    is_employed = forms.ChoiceField(choices=YES_NO_CHOICE,
                                    error_messages={'required': 'Please answer employment question.'})
    has_insurance = forms.ChoiceField(choices=YES_NO_CHOICE,
                                      error_messages={'required': 'Please answer insurancequestion.'})
    has_primary_doctor = forms.ChoiceField(choices=YES_NO_CHOICE,
                                           error_messages={'required': 'Please answer primary doctor question.'})


# defines dynamic form class for creating part 2 of risk assessment form.
# new fields created dynamically based on input from part 1
class AssessmentFormTwo(forms.Form):
    def __init__(self, previous_form_data, *args, **kwargs):
        super(AssessmentFormTwo, self).__init__(*args, **kwargs)

        if previous_form_data['has_heartdisease'] == 1:
            self.fields['heartdisease_over_10'] = forms.ChoiceField(choices=YES_NO_CHOICE, error_messages={
                'required': 'Please answer heart disease question.'})
        else:
            self.fields['has_history_of_heartdisease'] = forms.ChoiceField(choices=YES_NO_CHOICE, error_messages={
                'required': 'Please answer heart disease question.'})

        if previous_form_data['has_mentalillness'] == 1:
            self.fields['mental_illness_over_1'] = forms.ChoiceField(choices=YES_NO_CHOICE, error_messages={
                'required': 'Please answer mental illness question.'})
        else:
            self.fields['has_history_of_mentalillness'] = forms.ChoiceField(choices=YES_NO_CHOICE, error_messages={
                'required': 'Please answer mental illness question.'})

        if previous_form_data['does_smoke'] == 1:
            self.fields['smoke_atleast_a_pack_a_day'] = forms.ChoiceField(choices=YES_NO_CHOICE, error_messages={
                'required': 'Please answer smoking question.'})
