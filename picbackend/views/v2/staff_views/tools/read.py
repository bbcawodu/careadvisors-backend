"""
Defines utility functions and classes for staff views
"""

from picmodels.models import PICStaff
from picmodels.services import filter_staff_qset_by_id
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_f_and_l_name
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_first_name
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_last_name
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_email
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_mpn
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_county


def retrieve_staff_data_by_f_and_l_name(rqst_first_name, rqst_last_name, rqst_errors):
    staff_qset = filter_staff_objs_by_f_and_l_name(PICStaff.objects.all(), rqst_first_name, rqst_last_name)

    response_list = create_response_list_from_db_objects(staff_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No staff instances in db for given first and last name")

    check_response_data_for_requested_data()

    response_list = [response_list]

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_staff_data_by_email(list_of_emails, rqst_errors):
    response_list = []

    for email in list_of_emails:
        filtered_staff_qset = filter_staff_objs_by_email(PICStaff.objects.all(), email)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instance with email: {} not found in database'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_first_name(list_of_first_names, rqst_errors):
    response_list = []

    for first_name in list_of_first_names:
        filtered_staff_qset = filter_staff_objs_by_first_name(PICStaff.objects.all(), first_name)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instance with first name: {} not found in database'.format(first_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_last_name(list_of_last_names, rqst_errors):
    response_list = []

    for last_name in list_of_last_names:
        filtered_staff_qset = filter_staff_objs_by_last_name(PICStaff.objects.all(), last_name)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instance with last name: {} not found in database'.format(last_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_county(list_of_counties, rqst_errors):
    response_list = []

    for county in list_of_counties:
        filtered_staff_qset = filter_staff_objs_by_county(PICStaff.objects.all(), county)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instances with a default county of: {} not found in database'.format(county))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_region(list_of_regions, rqst_errors):
    response_list = []

    counties_mapped_to_regions = PICStaff.REGIONS
    for region in list_of_regions:
        if region not in counties_mapped_to_regions:
            rqst_errors.append("{} is not a valid region stored in the db.".format(region))
        else:
            counties_in_this_region = counties_mapped_to_regions[region]
            response_list_component = []

            for county in counties_in_this_region:
                def add_staff_data_from_county_to_response_component():
                    filtered_staff_qset = filter_staff_objs_by_county(PICStaff.objects.all(), county)

                    staff_data_for_this_county = create_response_list_from_db_objects(filtered_staff_qset)
                    for staff_data in staff_data_for_this_county:
                        response_list_component.append(staff_data)

                add_staff_data_from_county_to_response_component()

            def check_response_component_for_requested_data():
                if not response_list_component:
                    rqst_errors.append('Staff instances with a default county in region: {} not found in database'.format(region))

            check_response_component_for_requested_data()

            def add_response_component_to_response_data():
                if response_list_component:
                    response_list.append(response_list_component)

            add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_mpn(list_of_mpns, rqst_errors):
    response_list = []

    for mpn in list_of_mpns:
        filtered_staff_qset = filter_staff_objs_by_mpn(PICStaff.objects.all(), mpn)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instance with MPN: {} not found in database'.format(mpn))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_id(rqst_staff_id, list_of_ids, rqst_errors):
    staff_qset = filter_staff_qset_by_id(PICStaff.objects.all(), rqst_staff_id, list_of_ids)

    response_list = create_response_list_from_db_objects(staff_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No staff instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Staff instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list
