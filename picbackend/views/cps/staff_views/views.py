from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from picmodels.models import CPSStaff
from picmodels.forms import CPSStaffImageUploadForm
from picbackend.views.utils import validate_get_request_parameters
from picbackend.views.utils import init_v2_response_data
from picbackend.views.utils import JSONPUTRspMixin
from picbackend.views.utils import JSONGETRspMixin
from .tools import validate_staff_put_rqst_params


# Need to abstract common variables in get and post class methods into class attributes
class CPSStaffManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    def cps_staff_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_staff_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            staff_instance = None

            if rqst_action == "create":
                staff_instance = CPSStaff.create_staff_row_using_validated_params(validated_put_rqst_params, rqst_errors)
            elif rqst_action == "update":
                staff_instance = CPSStaff.modify_staff_row_using_validated_params(validated_put_rqst_params, rqst_errors)
            elif rqst_action == "delete":
                CPSStaff.delete_staff_row_using_validated_params(validated_put_rqst_params['rqst_usr_id'], rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["db_row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'Database Action' provided.")

            if staff_instance:
                response_raw_data['Data'] = {"db_row": staff_instance.return_values_dict()}

    def cps_staff_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'first_name' in validated_GET_rqst_params and 'last_name' in validated_GET_rqst_params:
                rqst_first_name = validated_GET_rqst_params['first_name']
                rqst_last_name = validated_GET_rqst_params['last_name']

                data_list = CPSStaff.retrieve_staff_data_by_f_and_l_name(rqst_first_name, rqst_last_name, rqst_errors)
            elif 'email' in validated_GET_rqst_params:
                list_of_emails = validated_GET_rqst_params['email_list']

                data_list = CPSStaff.retrieve_staff_data_by_email(list_of_emails, rqst_errors)
            elif 'first_name' in validated_GET_rqst_params:
                list_of_first_names = validated_GET_rqst_params['first_name_list']

                data_list = CPSStaff.retrieve_staff_data_by_first_name(list_of_first_names, rqst_errors)
            elif 'last_name' in validated_GET_rqst_params:
                list_of_last_names = validated_GET_rqst_params['last_name_list']

                data_list = CPSStaff.retrieve_staff_data_by_last_name(list_of_last_names, rqst_errors)
            elif 'county' in validated_GET_rqst_params:
                list_of_counties = validated_GET_rqst_params['county_list']

                data_list = CPSStaff.retrieve_staff_data_by_county(list_of_counties, rqst_errors)
            elif 'region' in validated_GET_rqst_params:
                list_of_regions = validated_GET_rqst_params['region_list']

                data_list = CPSStaff.retrieve_staff_data_by_region(list_of_regions, rqst_errors)
            elif 'id' in validated_GET_rqst_params:
                rqst_staff_id = validated_GET_rqst_params['id']
                if rqst_staff_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = CPSStaff.retrieve_staff_data_by_id(rqst_staff_id, list_of_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = cps_staff_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "first_name",
        "last_name",
        "email",
        "county",
        "region",
    ]
    parse_GET_request_and_add_response = cps_staff_management_get_logic


def upload_cps_staff_pic(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["id"], rqst_errors)

        if 'id' in search_params:
            rqst_staff_id = search_params['id']
            try:
                cps_staff_object = CPSStaff.objects.get(pk=rqst_staff_id)
                form = CPSStaffImageUploadForm(initial={'staff_id': cps_staff_object.id,
                                                        'cps_staff_pic': cps_staff_object.cps_staff_pic})
                return render(request, 'cps/cps_staff_image_upload_form.html', {'form': form})
            except CPSStaff.DoesNotExist:
                return HttpResponseForbidden("CPS Staff member not found for given id: {!s}".format(str(rqst_staff_id)))
        else:
            return HttpResponseForbidden("'id' must be in search parameters")
    if request.method == 'POST':
        form = CPSStaffImageUploadForm(request.POST, request.FILES)

        current_staff_instance_id = form.data['staff_id']
        try:
            cps_staff_object = CPSStaff.objects.get(id=current_staff_instance_id)
        except CPSStaff.DoesNotExist:
            HttpResponseForbidden("CPS Staff member not found for given id: {}".format(current_staff_instance_id))
        else:
            if request.POST.get('delete_current_image_field_value'):
                if cps_staff_object.cps_staff_pic:
                    cps_staff_object.cps_staff_pic.delete()

                return HttpResponse('Current image deleted.')
            elif form.is_valid():
                # Delete old pic
                if cps_staff_object.cps_staff_pic:
                    cps_staff_object.cps_staff_pic.delete()

                # Add new pic
                cps_staff_object.cps_staff_pic = form.cleaned_data['cps_staff_pic']
                cps_staff_object.save()
                return HttpResponse('image upload success')
            else:
                return render(request, 'cps/cps_staff_image_upload_form.html', {'form': form})
