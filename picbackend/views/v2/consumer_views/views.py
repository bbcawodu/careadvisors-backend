from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from picmodels.models import PICConsumer
from picmodels.models import PICConsumerBackup
from ..utils import clean_string_value_from_dict_object
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_consumer_data_by_f_and_l_name
from .tools import retrieve_consumer_data_by_email
from .tools import retrieve_consumer_data_by_first_name
from .tools import retrieve_consumer_data_by_last_name
from .tools import retrieve_consumer_data_by_id
from .tools import paginate_result_list_by_changing_excess_data_to_ids
from ..utils import JSONPUTRspMixin
from ..utils import JSONGETRspMixin
import sys


CONSUMERS_PER_PAGE = 20


# Need to abstract common variables in get and post class methods into class attributes
class ConsumerManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerManagementView, self).dispatch(request, *args, **kwargs)

    def consumer_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(rqst_body, "root", "Database Action", rqst_errors)

        # If there are no parsing errors, process POST data based on database action
        if not rqst_errors:
            if rqst_action == "Consumer Addition":
                matching_consumer_instances, consumer_instance, backup_consumer_obj = validate_rqst_params_and_add_instance(rqst_body, rqst_errors)

                if matching_consumer_instances:
                    consumer_match_data = []
                    for consumer in matching_consumer_instances:
                        consumer_match_data.append(consumer.return_values_dict())
                    response_raw_data['Data']['Possible Consumer Matches'] = consumer_match_data
                else:
                    if consumer_instance:
                        response_raw_data['Data']["Database ID"] = consumer_instance.id
                    if backup_consumer_obj:
                        response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()
            elif rqst_action == "Consumer Modification":
                consumer_instance, backup_consumer_obj = validate_rqst_params_and_modify_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    if consumer_instance:
                        response_raw_data['Data']["Database ID"] = consumer_instance.id
                    if backup_consumer_obj:
                        response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()
            elif rqst_action == "Consumer Deletion":
                backup_consumer_obj = validate_rqst_params_and_delete_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"

                    if backup_consumer_obj:
                        response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()
            else:
                rqst_errors.append("No valid 'Database Action' provided.")

    def consumer_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        # Retrieve all Patient Innovation Center consumer objects
        consumers = PICConsumer.objects.all()

        get_and_add_consumer_data_to_response(consumers, request, validated_GET_rqst_params, response_raw_data, rqst_errors)

    parse_PUT_request_and_add_response = consumer_management_put_logic

    accepted_GET_request_parameters = [
        "nav_id",
        "is_cps_consumer",
        "first_name",
        "last_name",
        "email",
        "id",
        "page"
    ]
    parse_GET_request_and_add_response = consumer_management_get_logic


# Need to abstract common variables in get and post class methods into class attributes
class ConsumerBackupManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer backup instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerBackupManagementView, self).dispatch(request, *args, **kwargs)

    def consumer_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        # Retrieve all Patient Innovation Center consumer objects
        consumers = PICConsumerBackup.objects.all()

        get_and_add_consumer_data_to_response(consumers, request, validated_GET_rqst_params, response_raw_data, rqst_errors)

    accepted_GET_request_parameters = [
        "nav_id",
        "is_cps_consumer",
        "first_name",
        "last_name",
        "email",
        "id",
        "page"
    ]
    parse_GET_request_and_add_response = consumer_management_get_logic


def get_and_add_consumer_data_to_response(consumers, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
    # Filter consumer objects based on GET parameters
    def filter_db_objects_by_secondary_params(db_objects):
        if 'nav_id_list' in validated_GET_rqst_params:
            list_of_nav_ids = validated_GET_rqst_params['nav_id_list']
            db_objects = db_objects.filter(navigator__in=list_of_nav_ids)
        if 'is_cps_consumer' in validated_GET_rqst_params:
            is_cps_consumer = validated_GET_rqst_params['is_cps_consumer']
            db_objects = db_objects.filter(cps_consumer=is_cps_consumer)

        return db_objects

    consumers = filter_db_objects_by_secondary_params(consumers)

    def retrieve_data_by_primary_params_and_add_to_response(db_objects):
        data_list = []

        if 'first_name' in validated_GET_rqst_params and 'last_name' in validated_GET_rqst_params:
            rqst_first_name = validated_GET_rqst_params['first_name']
            rqst_last_name = validated_GET_rqst_params['last_name']

            data_list = retrieve_consumer_data_by_f_and_l_name(db_objects, rqst_first_name, rqst_last_name, rqst_errors)
        elif 'email' in validated_GET_rqst_params:
            list_of_emails = validated_GET_rqst_params['email_list']

            data_list = retrieve_consumer_data_by_email(db_objects, list_of_emails, rqst_errors)
        elif 'first_name' in validated_GET_rqst_params:
            list_of_first_names = validated_GET_rqst_params['first_name_list']

            data_list = retrieve_consumer_data_by_first_name(db_objects, list_of_first_names, rqst_errors)
        elif 'last_name' in validated_GET_rqst_params:
            list_of_last_names = validated_GET_rqst_params['last_name_list']

            data_list = retrieve_consumer_data_by_last_name(db_objects, list_of_last_names, rqst_errors)
        elif 'id' in validated_GET_rqst_params:
            rqst_consumer_id = validated_GET_rqst_params['id']
            if rqst_consumer_id != 'all':
                list_of_ids = validated_GET_rqst_params['id_list']
            else:
                list_of_ids = None

            data_list = retrieve_consumer_data_by_id(db_objects, rqst_consumer_id, list_of_ids, rqst_errors)

            print('Retrieved and parsed consumer table data.')
            sys.stdout.flush()

            def paginate_results():
                rqst_page_no = validated_GET_rqst_params['page'] if 'page' in validated_GET_rqst_params else None
                base_url = request.build_absolute_uri(None)

                extra_urls = paginate_result_list_by_changing_excess_data_to_ids(data_list, CONSUMERS_PER_PAGE, rqst_page_no, base_url)
                if extra_urls:
                    response_raw_data['Page URLs'] = extra_urls

            paginate_results()

            print('Paginated Results.')
            sys.stdout.flush()
        else:
            rqst_errors.append('No Valid Parameters')

        response_raw_data['Data'] = data_list

    retrieve_data_by_primary_params_and_add_to_response(consumers)
