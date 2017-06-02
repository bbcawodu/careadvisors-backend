"""
This module defines views that handle carriers for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from ...utils import clean_string_value_from_dict_object
from ...utils import add_carrier
from ...utils import modify_carrier
from ...utils import delete_carrier
from ...utils import retrieve_id_carriers
from ...utils import retrieve_name_carriers
from ...utils import retrieve_state_carriers
from picmodels.models import HealthcareCarrier
from django.views.decorators.csrf import csrf_exempt
from ...base import JSONPUTRspMixin
from ...base import JSONGETRspMixin
from ...utils import build_search_params
from ...utils import init_v2_response_data
from picmodels.forms import CarrierSampleIDCardUploadForm
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings


#Need to abstract common variables in get and post class methods into class attributes
class CarriersManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CarriersManagementView, self).dispatch(request, *args, **kwargs)

    def carriers_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Carrier Addition":
                response_raw_data = add_carrier(response_raw_data, post_data, post_errors)
            elif rqst_action == "Carrier Modification":
                response_raw_data = modify_carrier(response_raw_data, post_data, post_errors)
            elif rqst_action == "Carrier Deletion":
                response_raw_data = delete_carrier(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def carriers_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        carriers = [HealthcareCarrier.objects.all()]

        def filter_results_by_secondary_params():
            if 'has_sample_id_card' in search_params:
                def filter_by_has_sample_id_card_param():
                    carriers_have_sample_id_cards = search_params['has_sample_id_card']

                    def filter_carriers_by_default_sample_id_card_url():
                        if carriers_have_sample_id_cards:
                            carriers[0] = carriers[0].exclude(sample_id_card=settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)
                        else:
                            carriers[0] = carriers[0].filter(sample_id_card=settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)
                    filter_carriers_by_default_sample_id_card_url()
                filter_by_has_sample_id_card_param()
        filter_results_by_secondary_params()

        if 'id' in search_params:
            rqst_carrier_id = search_params['id']
            if rqst_carrier_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_id_carriers(response_raw_data, rqst_errors, carriers[0],
                                                                   rqst_carrier_id, list_of_ids)
        elif 'name' in search_params:
            rqst_name = search_params['name']

            response_raw_data, rqst_errors = retrieve_name_carriers(response_raw_data, rqst_errors, carriers[0], rqst_name)
        elif 'state' in search_params:
            rqst_state = search_params['state']
            list_of_states = search_params['state list']

            response_raw_data, rqst_errors = retrieve_state_carriers(response_raw_data, rqst_errors, carriers[0],
                                                                     rqst_state, list_of_states)

        return response_raw_data, rqst_errors

    put_logic_function = carriers_management_put_logic
    get_logic_function = carriers_management_get_logic


def handle_carrier_sample_id_card_mgmt_rqst(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = build_search_params(request.GET, rqst_errors)

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

        if form.is_valid():
            try:
                carrier_object = HealthcareCarrier.objects.get(id=form.cleaned_data['carrier_id'])

                # Delete old pic
                if carrier_object.sample_id_card.url != (settings.MEDIA_URL + settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL):
                    carrier_object.sample_id_card.delete()
            except HealthcareCarrier.DoesNotExist:
                return HttpResponseForbidden("Healthcare carrier not found for given id: {}".format(form.cleaned_data['carrier_id']))

            carrier_object.sample_id_card = form.cleaned_data['sample_id_card']
            carrier_object.save()

            return HttpResponse(response_message)
        else:
            return render(request, 'carrier_sample_id_card_upload_form.html', {'form': form})
