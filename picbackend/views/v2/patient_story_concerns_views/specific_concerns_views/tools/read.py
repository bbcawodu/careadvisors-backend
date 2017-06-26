from picmodels.models import ConsumerGeneralConcern
from picmodels.services import filter_db_queryset_by_id
from picmodels.services.patient_story_models_services.consumer_specific_concern_services import filter_specific_concern_objs_by_question
from picmodels.services.patient_story_models_services.consumer_specific_concern_services import filter_specific_concern_objs_by_gen_concern_name
from picmodels.services.patient_story_models_services.consumer_specific_concern_services import filter_specific_concern_objs_by_gen_concern_id_subset


def retrieve_specific_concern_data_by_id(specific_concerns, rqst_specific_concern_id, list_of_ids, rqst_errors):
    specific_concerns = filter_db_queryset_by_id(specific_concerns, rqst_specific_concern_id, list_of_ids)

    response_list = create_response_list_from_db_objects(specific_concerns)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No specific concern instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in
                                                    response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Specific concern instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_specific_concern_data_by_question(specific_concerns, rqst_question, rqst_errors):
    specific_concerns = filter_specific_concern_objs_by_question(specific_concerns, rqst_question)

    response_list = create_response_list_from_db_objects(specific_concerns)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No specific concern instances in db for given question")

    check_response_data_for_requested_data()

    return response_list


def retrieve_specific_concern_data_by_gen_concern_name(specific_concerns, rqst_gen_concern_name, rqst_errors):
    specific_concerns = filter_specific_concern_objs_by_gen_concern_name(specific_concerns, rqst_gen_concern_name)

    response_list = create_response_list_from_db_objects(specific_concerns)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No specific concern instances in db for given general concern name.")

    check_response_data_for_requested_data()

    return response_list


def retrieve_specific_concern_data_by_gen_concern_id_subset(specific_concerns, list_of_gen_concern_ids, rqst_errors):
    specific_concerns = filter_specific_concern_objs_by_gen_concern_id_subset(specific_concerns, list_of_gen_concern_ids)

    response_list = create_response_list_from_db_objects(specific_concerns)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No specific concern instances in db for given subset of general concern ids.")

    check_response_data_for_requested_data()

    return response_list


def retrieve_specific_concern_data_by_gen_concern_id(list_of_gen_concern_ids, rqst_errors):
    response_list = []

    for gen_concern_id in list_of_gen_concern_ids:
        response_list_component = []

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        try:
            general_concern_instance = ConsumerGeneralConcern.objects.get(id=gen_concern_id)

            related_specific_concerns_qset = general_concern_instance.related_specific_concerns.all()
            response_list_component = create_response_list_from_db_objects(related_specific_concerns_qset)

            def check_response_data_for_requested_data():
                if not response_list_component:
                    rqst_errors.append("No related specific concern instances found in database for general concern id: {}".format(gen_concern_id))

            check_response_data_for_requested_data()

            add_response_component_to_response_data()
        except ConsumerGeneralConcern.DoesNotExist:
            rqst_errors.append("General concern instance does not exist for database id: {}".format(gen_concern_id))
            add_response_component_to_response_data()

    return response_list
