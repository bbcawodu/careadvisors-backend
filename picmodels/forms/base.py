"""
This file contains form classes for abstracting
forms across picbackend app
"""


from django.forms import Form
from django.forms import ImageField
from django.forms import FileField
from django.forms import HiddenInput
from django.forms import IntegerField
from django.forms import CharField


class NavigatorImageUploadForm(Form):
    """Image upload form."""
    staff_id = IntegerField(widget=HiddenInput())
    staff_pic = ImageField()

    # def __init__(self, *args, **kwargs):
    #     staff_id = kwargs.get('staff_id', None)
    #
    #     kwargs.update(initial={
    #         'staff_id': staff_id
    #     })
    #
    #     super(NavigatorImageUploadForm, self).__init__()


class NavResumeUploadForm(Form):
    """file upload form."""
    nav_id = IntegerField(widget=HiddenInput())
    nav_resume_file = FileField()


class CTAManagementForm(Form):
    """Image upload form."""
    cta_image = ImageField()
    cta_intent = CharField()


class CarrierSampleIDCardUploadForm(Form):
    """Image upload form."""
    carrier_id = IntegerField(widget=HiddenInput())
    sample_id_card = ImageField()
