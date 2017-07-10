"""
Defines views that handle Patient Innovation Center Staff based requests
API Version 2
"""


from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings
from picmodels.models import PICStaff
from picmodels.forms import StaffImageUploadForm
from ..utils import validate_get_request_parameters
from ..utils import init_v2_response_data
from ..utils import clean_string_value_from_dict_object
from ..utils import JSONPUTRspMixin
from ..utils import JSONGETRspMixin
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_staff_data_by_f_and_l_name
from .tools import retrieve_staff_data_by_email
from .tools import retrieve_staff_data_by_first_name
from .tools import retrieve_staff_data_by_last_name
from .tools import retrieve_staff_data_by_id
from .tools import retrieve_staff_data_by_mpn
from .tools import retrieve_staff_data_by_county
from .tools import retrieve_staff_data_by_region


# Need to abstract common variables in get and post class methods into class attributes
class StaffManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffManagementView, self).dispatch(request, *args, **kwargs)

    def staff_management_put_logic(self, post_data, response_raw_data, post_errors):
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        if not post_errors:
            staff_instance = None

            if rqst_action == "Staff Addition":
                staff_instance = validate_rqst_params_and_add_instance(post_data, post_errors)
            elif rqst_action == "Staff Modification":
                staff_instance = validate_rqst_params_and_modify_instance(post_data, post_errors)
            elif rqst_action == "Staff Deletion":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

            if staff_instance:
                response_raw_data['Data'] = {"Database ID": staff_instance.id}

    def staff_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'first name' in search_params and 'last name' in search_params:
                rqst_first_name = search_params['first name']
                rqst_last_name = search_params['last name']

                data_list = retrieve_staff_data_by_f_and_l_name(rqst_first_name, rqst_last_name, rqst_errors)
            elif 'email' in search_params:
                list_of_emails = search_params['email list']

                data_list = retrieve_staff_data_by_email(list_of_emails, rqst_errors)
            elif 'mpn' in search_params:
                list_of_mpns = search_params['mpn list']

                data_list = retrieve_staff_data_by_mpn(list_of_mpns, rqst_errors)
            elif 'first name' in search_params:
                list_of_first_names = search_params['first name list']

                data_list = retrieve_staff_data_by_first_name(list_of_first_names, rqst_errors)
            elif 'last name' in search_params:
                list_of_last_names = search_params['last name list']

                data_list = retrieve_staff_data_by_last_name(list_of_last_names, rqst_errors)
            elif 'county' in search_params:
                list_of_counties = search_params['county list']

                data_list = retrieve_staff_data_by_county(list_of_counties, rqst_errors)
            elif 'region' in search_params:
                list_of_regions = search_params['region list']

                data_list = retrieve_staff_data_by_region(list_of_regions, rqst_errors)
            elif 'id' in search_params:
                rqst_staff_id = search_params['id']
                if rqst_staff_id != 'all':
                    list_of_ids = search_params['id list']
                else:
                    list_of_ids = None

                data_list = retrieve_staff_data_by_id(rqst_staff_id, list_of_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list
            response_raw_data["s3_url"] = settings.AWS_S3_CUSTOM_DOMAIN

        retrieve_data_by_primary_params_and_add_to_response()

    put_logic_function = staff_management_put_logic

    accepted_get_parameters = [
        "id",
        "fname",
        "lname",
        "email",
        "mpn",
        "county",
        "region",
    ]
    get_logic_function = staff_management_get_logic


def upload_staff_pic(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["id"], rqst_errors)

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

        current_staff_instance_id = form.data['staff_id']
        try:
            staff_object = PICStaff.objects.get(id=current_staff_instance_id)
        except PICStaff.DoesNotExist:
            HttpResponseForbidden("Staff member not found for given id: {}".format(current_staff_instance_id))
        else:
            if request.POST.get('delete_current_image_field_value'):
                if staff_object.staff_pic:
                    staff_object.staff_pic.delete()

                return HttpResponse('Current image deleted.')
            elif form.is_valid():
                # Delete old pic
                if staff_object.staff_pic:
                    staff_object.staff_pic.delete()

                # Add new pic
                staff_object.staff_pic = form.cleaned_data['staff_pic']
                staff_object.save()
                return HttpResponse('image upload success')
            else:
                return render(request, 'staff_image_upload_form.html', {'form': form})
