from ...utils import clean_list_value_from_dict_object
from picmodels.models import ConsumerGeneralConcern
from math import ceil
from .constants import MAX_NO_OF_GEN_CONCERNS_GIVEN


def retrieve_related_spec_concern_objs_from_list_of_gen_concern_names(rqst_data, rqst_errors):
    list_of_related_specific_concern_qsets = []
    no_of_unique_rel_spec_concerns = 0

    # In python 2.X, the nonlocal keyword is not available to enable binding to non local variables in nested functions,
    # need to use this 'hack' to enable rebinding of a non local variable name.
    # More info here: https://stackoverflow.com/questions/2609518/python-nested-function-scopes
    unique_related_spec_concerns_qset = [None]

    rqst_ranked_general_concern_names = clean_list_value_from_dict_object(rqst_data, "root", "ranked_general_concerns",
                                                                          rqst_errors)
    if len(rqst_errors) == 0:
        no_of_ranked_gen_concerns = len(rqst_ranked_general_concern_names)

        if no_of_ranked_gen_concerns <= MAX_NO_OF_GEN_CONCERNS_GIVEN:
            def check_that_gen_concerns_are_strings():
                for indx, general_concern_name in enumerate(rqst_ranked_general_concern_names):
                    if not isinstance(general_concern_name, str):
                        rqst_errors.append(
                            "All ranked general concerns must be strings, ranked general concern is not an string for 'related_general_concerns' field at index: {}".format(
                                indx))

            check_that_gen_concerns_are_strings()

            def check_for_duplicates_in_gen_concerns():
                ranked_general_concerns_names_set = set(rqst_ranked_general_concern_names)
                if len(ranked_general_concerns_names_set) != len(rqst_ranked_general_concern_names):
                    rqst_errors.append(
                        "There are duplicates in the 'ranked_general_concerns' list. No duplicates allowed")

            check_for_duplicates_in_gen_concerns()

            if not rqst_errors:
                ranked_general_concerns_errors = []

                def get_related_specific_concerns_from_gen_concern_names():
                    for ranked_general_concerns_name in rqst_ranked_general_concern_names:
                        try:
                            ranked_general_concerns_object = ConsumerGeneralConcern.objects.get(
                                name__iexact=ranked_general_concerns_name)

                            related_spec_concerns_qset = ranked_general_concerns_object.related_specific_concerns.all().order_by(
                                "-research_weight")
                            if unique_related_spec_concerns_qset[0]:
                                unique_related_spec_concerns_qset[0] = unique_related_spec_concerns_qset[
                                                                           0] | related_spec_concerns_qset
                            else:
                                unique_related_spec_concerns_qset[0] = related_spec_concerns_qset

                            list_of_related_specific_concern_qsets.append(related_spec_concerns_qset)
                        except ConsumerGeneralConcern.DoesNotExist:
                            ranked_general_concerns_errors.append(
                                "No ConsumerGeneralConcern database entry found for name: {}".format(
                                    ranked_general_concerns_name))

                get_related_specific_concerns_from_gen_concern_names()

                def count_unique_related_specific_concerns():
                    return unique_related_spec_concerns_qset[0].distinct().count()

                if unique_related_spec_concerns_qset[0]:
                    no_of_unique_rel_spec_concerns = count_unique_related_specific_concerns()

                def add_general_concern_errors_to_request_errors():
                    for ranked_general_concerns_error in ranked_general_concerns_errors:
                        rqst_errors.append(ranked_general_concerns_error)

                add_general_concern_errors_to_request_errors()
        else:
            rqst_errors.append("Maximum number of ranked_general_concerns is {}, the number given is: {}".format(
                MAX_NO_OF_GEN_CONCERNS_GIVEN, no_of_ranked_gen_concerns))

    return list_of_related_specific_concern_qsets, no_of_unique_rel_spec_concerns


def calculate_number_of_specific_concerns_to_fill(no_of_gen_concern_objects, remaining_specific_concern_spots):
    # need to write formula to obtain percentage from no_of_gen_concern_objects and index in list
    percentage_of_specific_concern_sports_to_fill = (1 / no_of_gen_concern_objects) * \
                                                    calculate_weight_from_index_and_len_of_array(1,
                                                                                                 no_of_gen_concern_objects)
    no_of_specific_concerns_to_fill = ceil(
        percentage_of_specific_concern_sports_to_fill * remaining_specific_concern_spots)

    return no_of_specific_concerns_to_fill


def calculate_weight_from_index_and_len_of_array(indx, len_of_array):
    element_number = indx + 1
    if len_of_array == 1:
        return 1
    elif len_of_array == 2:
        if element_number == 1:
            return 1.7
        else:
            return .7
    elif len_of_array == 3:
        if element_number == 1:
            return 1.6
        elif element_number == 2:
            return .8
        else:
            return .8
    elif len_of_array == 4:
        if element_number == 1:
            return 1.5
        elif element_number == 2:
            return .9
        elif element_number == 3:
            return .8
        else:
            return .8
    elif len_of_array == 5:
        if element_number == 1:
            return 1.5
        elif element_number == 2:
            return .9
        elif element_number == 3:
            return .9
        elif element_number == 4:
            return .8
        else:
            return .8
    elif len_of_array == 6:
        if element_number == 1:
            return 1.4
        elif element_number == 2:
            return .9
        elif element_number == 3:
            return .9
        elif element_number == 4:
            return .9
        elif element_number == 5:
            return .9
        else:
            return .8
    else:
        return 1
