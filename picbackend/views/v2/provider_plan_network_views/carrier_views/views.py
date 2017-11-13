from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings
from picmodels.models import HealthcareCarrier
from picmodels.forms import CarrierSampleIDCardUploadForm
from ...utils import clean_string_value_from_dict_object
from ...utils import validate_get_request_parameters
from ...utils import init_v2_response_data
from ...utils import JSONPUTRspMixin
from ...utils import JSONGETRspMixin
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_carrier_data_by_id
from .tools import retrieve_carrier_data_by_name
from .tools import retrieve_carrier_data_by_state


# Need to abstract common variables in get and post class methods into class attributes
class CarriersManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def carriers_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(rqst_body, "root", "Database Action", rqst_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not rqst_errors:
            healthcare_carrier_obj = None
            if rqst_action == "Carrier Addition":
                healthcare_carrier_obj = validate_rqst_params_and_add_instance(rqst_body, rqst_errors)
            elif rqst_action == "Carrier Modification":
                healthcare_carrier_obj = validate_rqst_params_and_modify_instance(rqst_body, rqst_errors)
            elif rqst_action == "Carrier Deletion":
                validate_rqst_params_and_delete_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                rqst_errors.append("No valid 'Database Action' provided.")

            if healthcare_carrier_obj:
                response_raw_data['Data']["Database ID"] = healthcare_carrier_obj.id

    def carriers_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        carriers = [HealthcareCarrier.objects.all()]

        def filter_results_by_secondary_params():
            if 'has_sample_id_card' in validated_GET_rqst_params:
                def filter_by_has_sample_id_card_param():
                    carriers_have_sample_id_cards = validated_GET_rqst_params['has_sample_id_card']

                    def filter_carriers_by_default_sample_id_card_url():
                        if carriers_have_sample_id_cards:
                            carriers[0] = carriers[0].exclude(sample_id_card=settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)
                        else:
                            carriers[0] = carriers[0].filter(sample_id_card=settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)
                    filter_carriers_by_default_sample_id_card_url()
                filter_by_has_sample_id_card_param()
        filter_results_by_secondary_params()

        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_carrier_id = validated_GET_rqst_params['id']
                if rqst_carrier_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = retrieve_carrier_data_by_id(carriers[0], rqst_carrier_id, list_of_ids, rqst_errors)
            elif 'name' in validated_GET_rqst_params:
                rqst_name = validated_GET_rqst_params['name']

                data_list = retrieve_carrier_data_by_name(carriers[0], rqst_name, rqst_errors)
            elif 'state' in validated_GET_rqst_params:
                list_of_states = validated_GET_rqst_params['state_list']

                data_list = retrieve_carrier_data_by_state(carriers[0], list_of_states, rqst_errors)
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


def handle_carrier_sample_id_card_mgmt_rqst(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["id"], rqst_errors)

        if 'id' in search_params:
            rqst_carrier_id = search_params['id']

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
