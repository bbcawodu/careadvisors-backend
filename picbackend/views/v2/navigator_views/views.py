from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.clickjacking import xframe_options_exempt

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin
from picbackend.views.utils import init_v2_response_data
from picbackend.views.utils import validate_get_request_parameters
from picmodels.forms import NavigatorImageUploadForm
from picmodels.forms import NavResumeUploadForm
from picmodels.models import Navigators

import json

from .tools import validate_put_rqst_params
from .tools import validate_nav_sign_up_params


# Need to abstract common variables in get and post class methods into class attributes
class NavigatorManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    def navigator_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            navigator_row = None

            if rqst_action == "create":
                navigator_row = Navigators.create_row_w_validated_params(validated_put_rqst_params, rqst_errors)
            elif rqst_action == "update":
                navigator_row = Navigators.update_row_w_validated_params(validated_put_rqst_params, rqst_errors)
            elif rqst_action == "delete":
                Navigators.delete_row_w_validated_params(validated_put_rqst_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

            if navigator_row:
                response_raw_data['Data'] = {"row": navigator_row.return_values_dict()}

    def navigator_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'first_name' in validated_GET_rqst_params and 'last_name' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_f_and_l_name(validated_GET_rqst_params, rqst_errors)
            elif 'email' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_email(validated_GET_rqst_params, rqst_errors)
            elif 'mpn' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_mpn(validated_GET_rqst_params, rqst_errors)
            elif 'first_name' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_first_name(validated_GET_rqst_params, rqst_errors)
            elif 'last_name' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_last_name(validated_GET_rqst_params, rqst_errors)
            elif 'county' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_county(validated_GET_rqst_params, rqst_errors)
            elif 'region' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_region(validated_GET_rqst_params, rqst_errors)
            elif 'id' in validated_GET_rqst_params:
                data_list = Navigators.get_serialized_rows_by_id(validated_GET_rqst_params, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list
            response_raw_data["s3_url"] = settings.AWS_S3_CUSTOM_DOMAIN
            response_raw_data["url"] = request.build_absolute_uri()

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = navigator_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "approved_cm_client_id",
        "first_name",
        "last_name",
        "email",
        "mpn",
        "county",
        "region",
    ]
    parse_GET_request_and_add_response = navigator_management_get_logic


class NavigatorSignUpView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    def navigator_sign_up_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_params = validate_nav_sign_up_params(rqst_body, rqst_errors)
        rqst_action = validated_params['rqst_action']

        if not rqst_errors:
            navigator_row = None

            if rqst_action == "create":
                navigator_row = Navigators.create_row_w_validated_params(validated_params, rqst_errors)
            else:
                rqst_errors.append("No valid 'db_action' provided.")

            if navigator_row:
                response_raw_data['Data'] = {"row": navigator_row.return_values_dict()}

    def navigator_sign_up_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        pass

    parse_PUT_request_and_add_response = navigator_sign_up_put_logic

    accepted_GET_request_parameters = [

    ]
    parse_GET_request_and_add_response = navigator_sign_up_get_logic


@xframe_options_exempt
def upload_navigator_pic(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["id"], rqst_errors)

        if rqst_errors:
            return HttpResponseForbidden(json.dumps(rqst_errors))
        elif 'id' in search_params:
            rqst_staff_id = search_params['id_list'][0]
            try:
                staff_object = Navigators.objects.get(pk=rqst_staff_id)
                form = NavigatorImageUploadForm(
                    initial={
                        'staff_id': staff_object.id,
                        'staff_pic': staff_object.staff_pic
                    }
                )
                return render(
                    request,
                    'navigator_image_upload_form.html',
                    {
                        'form': form,
                        'url': request.build_absolute_uri()
                    }
                )
            except Navigators.DoesNotExist:
                return HttpResponseForbidden("Staff member not found for given id: {!s}".format(str(rqst_staff_id)))
        else:
            return HttpResponseForbidden("'id' must be in search parameters")
    if request.method == 'POST':
        form = NavigatorImageUploadForm(request.POST, request.FILES)

        current_staff_instance_id = form.data['staff_id']
        try:
            staff_object = Navigators.objects.get(id=current_staff_instance_id)
        except Navigators.DoesNotExist:
            HttpResponseForbidden("Staff member not found for given id: {}".format(current_staff_instance_id))
        else:
            if request.POST.get('delete_current_image_field_value'):
                if staff_object.staff_pic:
                    staff_object.staff_pic.delete()

                return render(
                    request,
                    'navigator_image_upload_success.html',
                    {
                        'message': 'Current image deleted.',
                    }
                )
            elif form.is_valid():
                # Delete old pic
                if staff_object.staff_pic:
                    staff_object.staff_pic.delete()

                # Add new pic
                staff_object.staff_pic = form.cleaned_data['staff_pic']
                staff_object.save()
                return render(
                    request,
                    'navigator_image_upload_success.html',
                    {
                        'message': 'image upload success',
                    }
                )
            else:
                return render(
                    request,
                    'navigator_image_upload_form.html',
                    {
                        'form': form,
                        'url': request.build_absolute_uri()
                    }
                )


@xframe_options_exempt
def upload_nav_resume(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["id"], rqst_errors)

        if rqst_errors:
            return HttpResponseForbidden(json.dumps(rqst_errors))
        elif 'id' in search_params:
            rqst_nav_id = search_params['id_list'][0]
            try:
                nav_row = Navigators.objects.get(pk=rqst_nav_id)
                form = NavResumeUploadForm(
                    initial={
                        'nav_id': nav_row.id,
                        'nav_resume_file': nav_row.resume_file
                    }
                )
                return render(
                    request,
                    'nav_resume_file_upload_form.html',
                    {
                        'form': form,
                        'url': request.build_absolute_uri()
                    }
                )
            except Navigators.DoesNotExist:
                return HttpResponseForbidden("Row in Navigators table not found for given id: {!s}".format(str(rqst_nav_id)))
        else:
            return HttpResponseForbidden("'id' must be in search parameters")
    if request.method == 'POST':
        form = NavResumeUploadForm(request.POST, request.FILES)

        current_nav_row_id = form.data['nav_id']
        try:
            nav_row = Navigators.objects.get(id=current_nav_row_id)
        except Navigators.DoesNotExist:
            HttpResponseForbidden("Row in Navigators table not found for given id: {}".format(current_nav_row_id))
        else:
            if request.POST.get('delete_current_resume_file_field_value'):
                if nav_row.resume_file:
                    nav_row.resume_file.delete()

                return render(
                    request,
                    'nav_resume_file_upload_result.html',
                    {
                        'message': 'Current resume_file deleted.',
                    }
                )
            elif form.is_valid():
                # Delete old pic
                if nav_row.resume_file:
                    nav_row.resume_file.delete()

                # Add new pic
                nav_row.resume_file = form.cleaned_data['nav_resume_file']
                nav_row.save()
                return render(
                    request,
                    'nav_resume_file_upload_result.html',
                    {
                        'message': 'resume_file upload success',
                    }
                )
            else:
                return render(
                    request,
                    'nav_resume_file_upload_form.html',
                    {
                        'form': form,
                        'url': request.build_absolute_uri()
                    }
                )
