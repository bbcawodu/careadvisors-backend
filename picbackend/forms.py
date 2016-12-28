"""
This file contains form classes for abstracting
forms across picbackend app
"""


from django.forms import ModelForm
from picmodels.models import NavMetricsLocation


class NavMetricsLocationForm(ModelForm):
    # country = ModelChoiceField(queryset=Country.objects.all(), empty_label="Choose Country", to_field_name="name")

    # def __init__(self, *args, **kwargs):
    #     super(NavMetricsLocationForm, self).__init__(*args, **kwargs)
    #     self.fields['country'].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = NavMetricsLocation
        fields = ["name", "address"]
