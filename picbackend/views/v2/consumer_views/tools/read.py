"""
Defines utility functions and classes for consumer views
"""


import math
import sys
from ..constants import CONSUMERS_PER_PAGE
from picmodels.models.care_advisors.consumer_models.services.read import filter_consumer_qset_by_id
from picmodels.models.care_advisors.consumer_models.services.read import filter_consumer_objs_by_f_and_l_name
from picmodels.models.care_advisors.consumer_models.services.read import filter_consumer_objs_by_email
from picmodels.models.care_advisors.consumer_models.services.read import filter_consumer_objs_by_first_name
from picmodels.models.care_advisors.consumer_models.services.read import filter_consumer_objs_by_last_name


def retrieve_consumer_data_by_id(consumers, rqst_consumer_id, list_of_ids, rqst_errors):
    consumers = filter_consumer_qset_by_id(consumers, rqst_consumer_id, list_of_ids)

    print('Finished db query.')
    sys.stdout.flush()

    response_list = create_response_list_from_db_objects(consumers)

    print('Built response data list.')
    sys.stdout.flush()

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No consumer instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Consumer instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    print('Parsed table data for missing entries.')
    sys.stdout.flush()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_consumer_data_by_f_and_l_name(consumers, rqst_first_name, rqst_last_name, rqst_errors):
    consumers = filter_consumer_objs_by_f_and_l_name(consumers, rqst_first_name, rqst_last_name)

    response_list = create_response_list_from_db_objects(consumers)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No consumers instances in db for given first and last name")

    check_response_data_for_requested_data()

    response_list = [response_list]

    return response_list


def retrieve_consumer_data_by_email(consumers, list_of_emails, rqst_errors):
    response_list = []

    for email in list_of_emails:
        filtered_consumers = filter_consumer_objs_by_email(consumers, email)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with email: {} not found in database'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_consumer_data_by_first_name(consumers, list_of_first_names, rqst_errors):
    response_list = []

    for first_name in list_of_first_names:
        filtered_consumers = filter_consumer_objs_by_first_name(consumers, first_name)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with first name: {} not found in database'.format(first_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_consumer_data_by_last_name(consumers, list_of_last_names, rqst_errors):
    response_list = []

    for last_name in list_of_last_names:
        filtered_consumers = filter_consumer_objs_by_last_name(consumers, last_name)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with last name: {} not found in database'.format(last_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def paginate_result_list_by_changing_excess_data_to_ids(result_list, rqst_page_no, base_url):
    page_urls = []

    def remove_all_keys_from_db_instance_info_dict_except_db_id(db_instance_info_dict):
        for key in list(db_instance_info_dict):
            if key != "Database ID":
                db_instance_info_dict.pop(key, None)

    def change_first_part_of_result_list_to_ids():
        first_part_of_consumer_list = list_of_consumer_info_objects[:end_point_of_first_list_to_change_to_ids]

        for consumer_instance_info in first_part_of_consumer_list:
            remove_all_keys_from_db_instance_info_dict_except_db_id(consumer_instance_info)

    def change_second_part_of_result_list_to_ids():
        second_part_of_consumer_list = list_of_consumer_info_objects[start_point_of_second_list_to_change_to_ids:]

        for consumer_instance_info in second_part_of_consumer_list:
            remove_all_keys_from_db_instance_info_dict_except_db_id(consumer_instance_info)

    def create_urls_for_other_paginatied_results():
        total_pages = math.ceil(len_of_consumer_list / CONSUMERS_PER_PAGE)

        for i in range(total_pages):
            page_urls.append(base_url + "&page=" + str(i + 1))

    list_of_consumer_info_objects = []
    for possible_consumer_info_sublist in result_list:
        if isinstance(possible_consumer_info_sublist, list):
            consumer_info_sublist = possible_consumer_info_sublist

            for consumer_info_object in consumer_info_sublist:
                list_of_consumer_info_objects.append(consumer_info_object)
        else:
            consumer_info_object = possible_consumer_info_sublist
            list_of_consumer_info_objects.append(consumer_info_object)

    len_of_consumer_list = len(list_of_consumer_info_objects)

    if len_of_consumer_list > CONSUMERS_PER_PAGE:
        if rqst_page_no:
            end_point_of_first_list_to_change_to_ids = ((rqst_page_no - 1) * CONSUMERS_PER_PAGE)
            start_point_of_second_list_to_change_to_ids = (rqst_page_no * CONSUMERS_PER_PAGE)

            if len_of_consumer_list > end_point_of_first_list_to_change_to_ids:
                change_first_part_of_result_list_to_ids()
            if len_of_consumer_list > start_point_of_second_list_to_change_to_ids:
                change_second_part_of_result_list_to_ids()
        else:
            create_urls_for_other_paginatied_results()

            start_point_of_second_list_to_change_to_ids = CONSUMERS_PER_PAGE
            change_second_part_of_result_list_to_ids()

    return page_urls
