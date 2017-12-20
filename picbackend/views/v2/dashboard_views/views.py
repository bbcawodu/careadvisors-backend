from django.conf import settings
import datetime
import jwt
from django.views.generic import View
from ..utils import JSONGETRspMixin


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
