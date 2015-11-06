"""
This file contains form classes for abstracting
forms across 
"""
from django import forms

YES_NO_CHOICE = [
    ('', 'Please Choose'),
    (0, 'No'),
    (1, 'Yes'),
]

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