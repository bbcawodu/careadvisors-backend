"""
Defines views that handle Patient Innovation Center consumer based requests
API Version 2
"""


from django.views.generic import View
from django.utils.decorators import method_decorator
from picmodels.models import PICConsumer
from picmodels.models import PICConsumerBackup
from django.views.decorators.csrf import csrf_exempt
from .utils import clean_string_value_from_dict_object
from .utils import add_consumer_using_api_rqst_params
from .utils import modify_consumer_using_api_rqst_params
from .utils import delete_consumer_using_api_rqst_params
from .utils import retrieve_f_l_name_consumers
from .utils import retrieve_email_consumers
from .utils import retrieve_first_name_consumers
from .utils import retrieve_last_name_consumers
from .utils import retrieve_id_consumers
from .utils import break_results_into_pages
from .base import JSONPUTRspMixin
from .base import JSONGETRspMixin


CONSUMERS_PER_PAGE = 20


# Need to abstract common variables in get and post class methods into class attributes
class ConsumerManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerManagementView, self).dispatch(request, *args, **kwargs)

    def consumer_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process POST data based on database action
        if not post_errors:
            if rqst_action == "Consumer Addition":
                response_raw_data = add_consumer_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Consumer Modification":
                response_raw_data = modify_consumer_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Consumer Deletion":
                response_raw_data = delete_consumer_using_api_rqst_params(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def consumer_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        # Retrieve all Patient Innovation Center consumer objects
        consumers = PICConsumer.objects.all()

        response_raw_data, rqst_errors = get_and_add_consumer_data_to_response(consumers, request, search_params, response_raw_data, rqst_errors)

        return response_raw_data, rqst_errors

    put_logic_function = consumer_management_put_logic
    get_logic_function = consumer_management_get_logic


# Need to abstract common variables in get and post class methods into class attributes
class ConsumerBackupManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer backup instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerBackupManagementView, self).dispatch(request, *args, **kwargs)

    def consumer_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        # Retrieve all Patient Innovation Center consumer objects
        consumers = PICConsumerBackup.objects.all()

        response_raw_data, rqst_errors = get_and_add_consumer_data_to_response(consumers, request, search_params, response_raw_data, rqst_errors)

        return response_raw_data, rqst_errors

    get_logic_function = consumer_management_get_logic


def get_and_add_consumer_data_to_response(consumers, request, search_params, response_raw_data, rqst_errors):
    # Filter consumer objects based on GET parameters
    if 'navigator id list' in search_params:
        list_of_nav_ids = search_params['navigator id list']
        consumers = consumers.filter(navigator__in=list_of_nav_ids)
    if 'is_cps_consumer' in search_params:
        is_cps_consumer = search_params['is_cps_consumer']
        consumers = consumers.filter(cps_consumer=is_cps_consumer)

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

    return response_raw_data, rqst_errors