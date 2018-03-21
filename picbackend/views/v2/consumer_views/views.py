import sys

from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import PICConsumer
from picmodels.models import PICConsumerBackup

from .tools import validate_put_rqst_params
from .tools import paginate_result_list_by_changing_excess_data_to_ids


# Need to abstract common variables in get and post class methods into class attributes
class ConsumerManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center consumer instance related requests
    """

    def consumer_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            if rqst_action == "create":
                matching_consumer_instances, consumer_instance, backup_consumer_obj = PICConsumer.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if matching_consumer_instances:
                    consumer_match_data = []
                    for consumer in matching_consumer_instances:
                        consumer_match_data.append(consumer.return_values_dict())
                    response_raw_data['Status']['Possible Consumer Matches'] = consumer_match_data
                else:
                    if consumer_instance:
                        response_raw_data['Data']["row"] = consumer_instance.return_values_dict()
                    if backup_consumer_obj:
                        response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()
            elif rqst_action == "update":
                consumer_instance, backup_consumer_obj = PICConsumer.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if not rqst_errors:
                    if consumer_instance:
                        response_raw_data['Data']["row"] = consumer_instance.return_values_dict()
                    if backup_consumer_obj:
                        response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()
            elif rqst_action == "delete":
                backup_consumer_obj = PICConsumer.delete_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"

                    if backup_consumer_obj:
                        response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def consumer_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        get_and_add_consumer_data_to_response(
            request,
            PICConsumer,
            validated_GET_rqst_params,
            response_raw_data,
            rqst_errors
        )

    parse_PUT_request_and_add_response = consumer_management_put_logic

    accepted_GET_request_parameters = [
        "nav_id",
        "is_cps_consumer",
        "has_hospital_info",
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

    def consumer_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        get_and_add_consumer_data_to_response(
            request,
            PICConsumerBackup,
            validated_GET_rqst_params,
            response_raw_data,
            rqst_errors
        )

    accepted_GET_request_parameters = [
        "nav_id",
        "is_cps_consumer",
        "has_hospital_info",
        "first_name",
        "last_name",
        "email",
        "id",
        "page"
    ]
    parse_GET_request_and_add_response = consumer_management_get_logic


def get_and_add_consumer_data_to_response(request, db_model, validated_GET_rqst_params, response_raw_data, rqst_errors):
    def retrieve_data_by_primary_params_and_add_to_response(db_model_class):
        data_list = []

        def paginate_results():
            rqst_page_no = validated_GET_rqst_params['page'] if 'page' in validated_GET_rqst_params else None
            base_url = request.build_absolute_uri(None)

            extra_urls = paginate_result_list_by_changing_excess_data_to_ids(data_list, rqst_page_no, base_url)
            if extra_urls:
                response_raw_data['Page URLs'] = extra_urls

        if 'first_name' in validated_GET_rqst_params and 'last_name' in validated_GET_rqst_params:
            data_list = db_model_class.get_serialized_rows_by_f_and_l_name(validated_GET_rqst_params, rqst_errors)
        elif 'email' in validated_GET_rqst_params:
            data_list = db_model_class.get_serialized_rows_by_email(validated_GET_rqst_params, rqst_errors)
        elif 'first_name' in validated_GET_rqst_params:
            data_list = db_model_class.get_serialized_rows_by_first_name(validated_GET_rqst_params, rqst_errors)
        elif 'last_name' in validated_GET_rqst_params:
            data_list = db_model_class.get_serialized_rows_by_last_name(validated_GET_rqst_params, rqst_errors)
        elif 'id' in validated_GET_rqst_params:
            data_list = db_model_class.get_serialized_rows_by_id(validated_GET_rqst_params, rqst_errors)
        else:
            rqst_errors.append('No Valid Parameters')

        print('Retrieved and parsed consumer table data.')
        sys.stdout.flush()

        paginate_results()

        print('Paginated Results.')
        sys.stdout.flush()

        response_raw_data['Data'] = data_list

    retrieve_data_by_primary_params_and_add_to_response(db_model)
