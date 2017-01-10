"""
Defines views that handle Patient Innovation Center Staff based requests
API Version 2
"""


from django.views import View
from django.utils.decorators import method_decorator
from picmodels.models import PICStaff
from django.views.decorators.csrf import csrf_exempt
from .utils import build_search_params
from .utils import init_v2_response_data
from .utils import clean_string_value_from_dict_object
from .utils import add_staff
from .utils import modify_staff
from .utils import delete_staff
from .utils import retrieve_f_l_name_staff
from .utils import retrieve_email_staff
from .utils import retrieve_first_name_staff
from .utils import retrieve_last_name_staff
from .utils import retrieve_id_staff
from .utils import retrieve_mpn_staff
from .utils import retrieve_county_staff
from .utils import retrieve_region_staff
from .base import JSONPUTRspMixin
from .base import JSONGETRspMixin
from picmodels.forms import StaffImageUploadForm
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .utils import parse_and_log_errors


# Need to abstract common variables in get and post class methods into class attributes
@method_decorator(csrf_exempt, name='dispatch')
class StaffManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    def staff_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Code to parse POSTed json request
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0 and rqst_action == "Staff Addition":
            response_raw_data = add_staff(response_raw_data, post_data, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Staff Modification":
            response_raw_data = modify_staff(response_raw_data, post_data, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Staff Deletion":
            response_raw_data = delete_staff(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def staff_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        staff_members = PICStaff.objects.all()

        if 'first name' in search_params and 'last name' in search_params:
            rqst_first_name = search_params['first name']
            rqst_last_name = search_params['last name']
            response_raw_data, rqst_errors = retrieve_f_l_name_staff(response_raw_data, rqst_errors, staff_members,
                                                                     rqst_first_name, rqst_last_name)
        elif 'email' in search_params:
            rqst_email = search_params['email']
            list_of_emails = search_params['email list']
            response_raw_data, rqst_errors = retrieve_email_staff(response_raw_data, rqst_errors, rqst_email,
                                                                  list_of_emails)
        elif 'mpn' in search_params:
            rqst_mpn = search_params['mpn']
            list_of_mpns = search_params['mpn list']
            response_raw_data, rqst_errors = retrieve_mpn_staff(response_raw_data, rqst_errors, rqst_mpn,
                                                                  list_of_mpns)
        elif 'first name' in search_params:
            rqst_first_name = search_params['first name']
            list_of_first_names = search_params['first name list']
            response_raw_data, rqst_errors = retrieve_first_name_staff(response_raw_data, rqst_errors, rqst_first_name,
                                                                       list_of_first_names)
        elif 'last name' in search_params:
            rqst_last_name = search_params['last name']
            list_of_last_names = search_params['last name list']
            response_raw_data, rqst_errors = retrieve_last_name_staff(response_raw_data, rqst_errors, rqst_last_name,
                                                                      list_of_last_names)
        elif 'county' in search_params:
            rqst_county = search_params['county']
            list_of_counties = search_params['county list']
            response_raw_data, rqst_errors = retrieve_county_staff(response_raw_data, rqst_errors, rqst_county,
                                                                   list_of_counties)
        elif 'region' in search_params:
            rqst_region = search_params['region']
            list_of_regions = search_params['region list']
            response_raw_data, rqst_errors = retrieve_region_staff(response_raw_data, rqst_errors, rqst_region,
                                                                   list_of_regions)
        elif 'id' in search_params:
            rqst_staff_id = search_params['id']
            if rqst_staff_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_id_staff(response_raw_data, rqst_errors, rqst_staff_id, list_of_ids)
        else:
            rqst_errors.append('No Valid Parameters')

        return response_raw_data, rqst_errors

    put_logic_function = staff_management_put_logic
    get_logic_function = staff_management_get_logic


def upload_staff_pic(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = build_search_params(request.GET, response_raw_data, rqst_errors)
        if 'id' in search_params:
            rqst_staff_id = search_params['id']
            try:
                staff_object = PICStaff.objects.get(pk=rqst_staff_id)
                form = StaffImageUploadForm(initial={'staff_id': staff_object.id,
                                                     'staff_pic': staff_object.staff_pic})
                return render(request, 'staff_image_upload_form.html', {'form': form})
            except PICStaff.DoesNotExist:
                return HttpResponseForbidden("Staff member not found for given id: {!s}".format(str(rqst_staff_id)))
        else:
            return HttpResponseForbidden("'id' must be in search parameters")
    if request.method == 'POST':
        form = StaffImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            staff_object = PICStaff.objects.get(id=form.cleaned_data['staff_id'])
            staff_object.staff_pic = form.cleaned_data['staff_pic']
            staff_object.save()
            return HttpResponse('image upload success')