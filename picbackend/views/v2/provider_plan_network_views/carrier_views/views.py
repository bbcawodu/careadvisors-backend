from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.clickjacking import xframe_options_exempt

from picmodels.models import HealthcareCarrier

import json

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin
from picbackend.views.utils import init_v2_response_data
from picbackend.views.utils import validate_get_request_parameters

from .tools import validate_put_rqst_params

from picmodels.forms import CarrierSampleIDCardUploadForm


# Need to abstract common variables in get and post class methods into class attributes
class CarriersManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def carriers_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        # If there are no parsing errors, process PUT data based on database action
        if not rqst_errors:
            healthcare_carrier_obj = None
            if rqst_action == "create":
                healthcare_carrier_obj = HealthcareCarrier.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )
            elif rqst_action == "update":
                healthcare_carrier_obj = HealthcareCarrier.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )
            elif rqst_action == "delete":
                HealthcareCarrier.delete_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

            if healthcare_carrier_obj:
                response_raw_data['Data']["row"] = healthcare_carrier_obj.return_values_dict()

    def carriers_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                data_list = HealthcareCarrier.get_serialized_rows_by_id(validated_GET_rqst_params, rqst_errors)
            elif 'name' in validated_GET_rqst_params:
                data_list = HealthcareCarrier.get_serialized_rows_by_name(validated_GET_rqst_params, rqst_errors)
            elif 'state' in validated_GET_rqst_params:
                data_list = HealthcareCarrier.get_serialized_rows_by_state(validated_GET_rqst_params, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = carriers_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "name",
        "state",
        "has_sample_id_card"
    ]
    parse_GET_request_and_add_response = carriers_management_get_logic


@xframe_options_exempt
def handle_carrier_sample_id_card_mgmt_rqst(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["id"], rqst_errors)

        if rqst_errors:
            return HttpResponseForbidden(json.dumps(rqst_errors))
        elif 'id' in search_params:
            rqst_carrier_id = search_params['id_list'][0]

            try:
                carrier_object = HealthcareCarrier.objects.get(id=rqst_carrier_id)
                form = CarrierSampleIDCardUploadForm(initial={'carrier_id': carrier_object.id,
                                                              'sample_id_card': carrier_object.sample_id_card})

                return render(request, 'carrier_sample_id_card_upload_form.html', {'form': form})
            except HealthcareCarrier.DoesNotExist:
                return HttpResponseForbidden("Healthcare carrier not found for given id: {}".format(rqst_carrier_id))
        else:
            return HttpResponseForbidden("'id' must be in search parameters")

    if request.method == 'POST':
        response_message = 'Sample id card image edit success!'
        form = CarrierSampleIDCardUploadForm(request.POST, request.FILES)

        if request.POST.get('delete_current_image_field_value'):
            current_carrier_id = form.data['carrier_id']
            try:
                carrier_object = HealthcareCarrier.objects.get(id=current_carrier_id)
            except HealthcareCarrier.DoesNotExist:
                HttpResponseForbidden("Healthcare carrier not found for given id: {}".format(current_carrier_id))
            else:
                if carrier_object.sample_id_card:
                    carrier_object.sample_id_card.delete()

                return HttpResponse('Current image deleted.')
        elif form.is_valid():
            try:
                carrier_object = HealthcareCarrier.objects.get(id=form.cleaned_data['carrier_id'])

                # Delete old pic
                if carrier_object.sample_id_card:
                    carrier_object.sample_id_card.delete()
            except HealthcareCarrier.DoesNotExist:
                return HttpResponseForbidden("Healthcare carrier not found for given id: {}".format(form.cleaned_data['carrier_id']))

            carrier_object.sample_id_card = form.cleaned_data['sample_id_card']
            carrier_object.save()

            return HttpResponse(response_message)
        else:
            return render(request, 'carrier_sample_id_card_upload_form.html', {'form': form})
