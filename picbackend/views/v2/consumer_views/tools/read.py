"""
Defines utility functions and classes for consumer views
"""


import math
from ..constants import CONSUMERS_PER_PAGE


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
