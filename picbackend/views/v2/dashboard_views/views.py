import datetime

import jwt
import json
from django.conf import settings
from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin

from django.http import HttpResponseForbidden
from django.shortcuts import render
from picmodels.models import CPSStaff
from picbackend.views.utils import validate_get_request_parameters
from picbackend.views.utils import init_v2_response_data


# Need to abstract common variables in get and post class methods into class attributes
class DashboardView(JSONGETRspMixin, View):
    def dashboard_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        payload = {
            'dashboard': 199534,
            'organization': 32342,
            'env': {"MYVAR": 42}
        }
        token = jwt.generate_jwt(payload, settings.CHARTIO_ORG_SECRET, 'HS256',
                                 datetime.timedelta(days=1))
        iframe_src_url = '%s/%s' % (settings.CHARTIO_BASE_URL, token)

        response_raw_data['iframe_url'] = iframe_src_url

    accepted_GET_request_parameters = []
    parse_GET_request_and_add_response = dashboard_get_logic


def render_demo_dashboard(request):
    if request.method == 'GET':
        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["id"], rqst_errors)

        if rqst_errors:
            return HttpResponseForbidden(json.dumps(rqst_errors))
        elif 'id' in search_params:
            rqst_staff_id = search_params['id_list'][0]
            try:
                cps_staff_object = CPSStaff.objects.get(pk=rqst_staff_id)
                return render(request, 'dashboard_demo_view.html')
            except CPSStaff.DoesNotExist:
                return HttpResponseForbidden("CPS Staff member not found for given id: {!s}".format(str(rqst_staff_id)))
        else:
            return HttpResponseForbidden("'id' must be in search parameters")
