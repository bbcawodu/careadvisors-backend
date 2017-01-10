"""
This file contains form classes for abstracting
forms across picbackend app
"""


from django.forms import ModelForm
from django.forms import Form
from django.forms import ImageField
from django.forms import HiddenInput
from django.forms import IntegerField
from .models import PICStaff


# class StaffImageUploadForm(ModelForm):
#     temp_id = IntegerField()
#
#     """Image upload form."""
#     class Meta:
#         model = PICStaff
#         fields = ['staff_pic']
#
#     def save(self, commit=True):
#         staff_object = PICStaff.objects.get(id=self.cleaned_data['temp_id'])
#         staff_object.staff_pic = self.cleaned_data['staff_pic']
#         staff_object.save()
#         # do something with self.cleaned_data['temp_id']
#         return super(StaffImageUploadForm, self).save(commit=commit)

class StaffImageUploadForm(Form):
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
    #     super(StaffImageUploadForm, self).__init__()
