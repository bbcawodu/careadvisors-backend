from picmodels.services import filter_db_queryset_by_id
from picmodels.services import filter_healthcare_subsidy_eligibility_data_instances_by_family_size


def retrieve_healthcare_subsidy_eligibility_data_by_id(healthcare_subsidy_eligibility_data_objs, rqst_healthcare_subsidy_eligibility_data_id, list_of_ids, rqst_errors):
    healthcare_subsidy_eligibility_data_objs = filter_db_queryset_by_id(healthcare_subsidy_eligibility_data_objs, rqst_healthcare_subsidy_eligibility_data_id, list_of_ids)

    response_list = create_response_list_from_db_objects(healthcare_subsidy_eligibility_data_objs)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No healthcare subsidy eligibility data instances in db for given ids")
        else:
            if list_of_ids:
                for healthcare_subsidy_eligibility_data_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == healthcare_subsidy_eligibility_data_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Healthcare subsidy eligibility data instance with id: {} not found in database'.format(healthcare_subsidy_eligibility_data_id))

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_healthcare_subsidy_eligibility_data_by_family_size(healthcare_subsidy_eligibility_data_objs, list_of_family_sizes, rqst_errors):
    healthcare_subsidy_eligibility_data_objs = filter_healthcare_subsidy_eligibility_data_instances_by_family_size(healthcare_subsidy_eligibility_data_objs, list_of_family_sizes)

    response_list = create_response_list_from_db_objects(healthcare_subsidy_eligibility_data_objs)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No healthcare subsidy eligibility data instances in db for given family sizes.")
        for family_size in list_of_family_sizes:
            tuple_of_bools_if_family_size_in_data = (instance_data['family_size'] == family_size for instance_data in response_list)
            if not any(tuple_of_bools_if_family_size_in_data):
                rqst_errors.append('Healthcare subsidy eligibility data instance with family size: {} not found in database'.format(family_size))

    check_response_data_for_requested_data()

    return response_list
