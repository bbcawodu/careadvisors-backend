from picmodels.models import CallToAction
from .utils import build_search_params
from .utils import init_v2_response_data
from picmodels.forms import CTAManagementForm
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings
from django.views.generic import View
from .base import JSONGETRspMixin


def manage_cta_request(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = build_search_params(request.GET, rqst_errors)
        cta_messages = []
        form = CTAManagementForm()

        if 'intent' in search_params:
            rqst_cta_intent = search_params['intent']

            try:
                cta_object = CallToAction.objects.get(intent__iexact=rqst_cta_intent)
                form = CTAManagementForm(initial={'cta_intent': cta_object.intent,
                                                  'cta_image': cta_object.cta_image})
            except CallToAction.DoesNotExist:
                cta_messages.append("New Call to Action!")

        return render(request, 'cta_management_form.html', {'form': form,
                                                            "cta_messages": cta_messages})
    if request.method == 'POST':
        response_message = 'cta object edit success!'
        form = CTAManagementForm(request.POST, request.FILES)

        if form.is_valid():
            form.cleaned_data['cta_intent'] = form.cleaned_data['cta_intent'].lower()
            try:
                cta_object = CallToAction.objects.get(intent__iexact=form.cleaned_data['cta_intent'])

                # Delete old pic
                if cta_object.cta_image.url != (settings.MEDIA_URL + settings.DEFAULT_CTA_PIC_URL):
                    cta_object.cta_image.delete()
            except CallToAction.DoesNotExist:
                cta_object = CallToAction(intent=form.cleaned_data['cta_intent'])
                response_message = 'new cta created! success!'

            cta_object.cta_image = form.cleaned_data['cta_image']
            cta_object.save()

            return HttpResponse(response_message)
        else:
            return render(request, 'cta_management_form.html', {'form': form})


# Need to abstract common variables in get and post class methods into class attributes
class ViewCTAView(JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center navigator hub location instance related requests
    """

    def view_cta_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        cta_return_list = []
        if 'intent' in search_params:
            try:
                if search_params['intent'] == 'all':
                    cta_objects = CallToAction.objects.all()

                    for cta_object in cta_objects:
                        cta_return_list.append(cta_object.return_values_dict())
                else:
                    cta_object = CallToAction.objects.get(intent__iexact=search_params['intent'])

                    cta_return_list.append(cta_object.return_values_dict())
            except CallToAction.DoesNotExist:
                rqst_errors.append("No Call to Action object found for intent keyword: {}".format(search_params["intent"]))
        else:
            rqst_errors.append("'intent' must be in GET parameters")

        response_raw_data["Data"] = cta_return_list

        return response_raw_data, rqst_errors

    get_logic_function = view_cta_get_logic
