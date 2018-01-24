from django.forms import Form
from django.forms import ImageField
from django.forms import HiddenInput
from django.forms import IntegerField


class CPSStaffImageUploadForm(Form):
    """Image upload form."""
    staff_id = IntegerField(widget=HiddenInput())
    cps_staff_pic = ImageField()

    # def __init__(self, *args, **kwargs):
    #     staff_id = kwargs.get('staff_id', None)
    #
    #     kwargs.update(initial={
    #         'staff_id': staff_id
    #     })
    #
    #     super(StaffImageUploadForm, self).__init__()