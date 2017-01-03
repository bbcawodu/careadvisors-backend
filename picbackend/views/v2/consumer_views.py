"""
Defines views that handle Patient Innovation Center consumer based requests
API Version 2
"""

from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from picmodels.models import PICConsumer
import json
from django.views.decorators.csrf import csrf_exempt
from .utils import build_search_params
from .utils import clean_json_string_input
from .utils import init_v2_response_data
from .utils import parse_and_log_errors
from .utils import add_consumer
from .utils import modify_consumer
from .utils import delete_consumer
from .utils import retrieve_f_l_name_consumers
from .utils import retrieve_email_consumers
from .utils import retrieve_first_name_consumers
from .utils import retrieve_last_name_consumers
from .utils import retrieve_id_consumers
from .utils import break_results_into_pages


CONSUMERS_PER_PAGE = 20


#Need to abstract common variables in get and post class methods into class attributes
@method_decorator(csrf_exempt, name='dispatch')
class ConsumerManagementView(View):
    def put(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center consumer instance edit requests
        :param request: django request instance object
        :rtype: HttpResponse
        """

        # Initialize dictionary for response data, initialize list for parsing errors
        response_raw_data, post_errors = init_v2_response_data()

        post_json = request.body.decode('utf-8')
        post_data = json.loads(post_json)

        # Retrieve database action from post data
        rqst_action = clean_json_string_input(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process POST data based on database action
        if not post_errors:
            if rqst_action == "Consumer Addition":
                response_raw_data = add_consumer(response_raw_data, post_data, post_errors)
            elif rqst_action == "Consumer Modification":
                response_raw_data = modify_consumer(response_raw_data, post_data, post_errors)
            elif rqst_action == "Consumer Deletion":
                response_raw_data = delete_consumer(response_raw_data, post_data, post_errors)

        response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        return response

    def get(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center consumer instance api retrieval requests
        :param request: django request instance object
        :rtype: HttpResponse
        """

        # Initialize dictionary for response data, initialize list for parsing errors
        response_raw_data, rqst_errors = init_v2_response_data()

        # Build dictionary that contains valid Patient Innovation Center GET parameters
        search_params = build_search_params(request.GET, response_raw_data, rqst_errors)

        # Retrieve all Patient Innovation Center consumer objects
        consumers = PICConsumer.objects.all()

        # Filter consumer objects based on GET parameters
        if 'navigator id list' in search_params:
            list_of_nav_ids = search_params['navigator id list']
            consumers = consumers.filter(navigator__in=list_of_nav_ids)
        if 'first name' in search_params and 'last name' in search_params:
            rqst_first_name = search_params['first name']
            rqst_last_name = search_params['last name']
            response_raw_data, rqst_errors = retrieve_f_l_name_consumers(response_raw_data, rqst_errors, consumers,
                                                                         rqst_first_name, rqst_last_name)
        elif 'email' in search_params:
            rqst_email = search_params['email']
            list_of_emails = search_params['email list']
            response_raw_data, rqst_errors = retrieve_email_consumers(response_raw_data, rqst_errors, consumers, rqst_email,
                                                                      list_of_emails)
        elif 'first name' in search_params:
            rqst_first_name = search_params['first name']
            list_of_first_names = search_params['first name list']
            response_raw_data, rqst_errors = retrieve_first_name_consumers(response_raw_data, rqst_errors, consumers,
                                                                           rqst_first_name, list_of_first_names)
        elif 'last name' in search_params:
            rqst_last_name = search_params['last name']
            list_of_last_names = search_params['last name list']
            response_raw_data, rqst_errors = retrieve_last_name_consumers(response_raw_data, rqst_errors, consumers,
                                                                          rqst_last_name, list_of_last_names)
        elif 'id' in search_params:
            rqst_consumer_id = search_params['id']
            if rqst_consumer_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_id_consumers(response_raw_data, rqst_errors, consumers,
                                                                   rqst_consumer_id, list_of_ids)
        else:
            rqst_errors.append('No Valid Parameters')

        # Break consumer results into pages so that results aren't too unruly
        if "Data" in response_raw_data:
            rqst_page_no = search_params['page number'] if 'page number' in search_params else None
            response_raw_data = break_results_into_pages(request, response_raw_data, CONSUMERS_PER_PAGE, rqst_page_no)

        response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        return response