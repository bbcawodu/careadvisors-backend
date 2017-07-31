from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ...utils import JSONPOSTRspMixin
from copy import deepcopy
from .tools import retrieve_related_spec_concern_objs_from_list_of_gen_concern_names
from .tools import calculate_number_of_specific_concerns_to_fill
from .constants import MIN_NO_OF_SPECIFIC_CONCERNS_TO_FETCH


# Need to abstract common variables in get and post class methods into class attributes
class RankedSpecificConcernsView(JSONPOSTRspMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RankedSpecificConcernsView, self).dispatch(request, *args, **kwargs)

    def ranked_specific_concerns_post_logic(self, rqst_body, response_raw_data, rqst_errors):
        list_of_related_specific_concern_qsets, no_of_unique_rel_spec_concerns = retrieve_related_spec_concern_objs_from_list_of_gen_concern_names(rqst_body, rqst_errors)
        if no_of_unique_rel_spec_concerns == 0:
            rqst_errors.append(
                "There are no related specific concern objects in the db for the given general concerns.")

        if not rqst_errors:
            def determine_min_no_of_specific_concerns_to_fetch():
                if no_of_unique_rel_spec_concerns < MIN_NO_OF_SPECIFIC_CONCERNS_TO_FETCH:
                    return no_of_unique_rel_spec_concerns
                else:
                    return MIN_NO_OF_SPECIFIC_CONCERNS_TO_FETCH

            min_no_of_specific_concerns_to_fetch = determine_min_no_of_specific_concerns_to_fetch()
            response_raw_data["min_entries"] = min_no_of_specific_concerns_to_fetch

            ranked_list_of_specific_concern_objects = []

            def compile_ranked_list_of_specific_concern_objects(ordered_list_of_spec_conc_qsets):
                no_of_gen_concern_objects = len(ordered_list_of_spec_conc_qsets)
                remaining_specific_concern_spots = min_no_of_specific_concerns_to_fetch - len(
                    ranked_list_of_specific_concern_objects)

                if ordered_list_of_spec_conc_qsets:
                    # Need a copy of all the objects within the list. This is because lists and querysets are mutable
                    # and all changes will be propagated to the original list. I do not want this. Original list should
                    # remain intact
                    ordered_list_of_spec_conc_qsets = deepcopy(ordered_list_of_spec_conc_qsets)

                    if len(ranked_list_of_specific_concern_objects) < min_no_of_specific_concerns_to_fetch:
                        related_specific_concern_qset = ordered_list_of_spec_conc_qsets[0]
                        for ranked_specific_concern_entry in ranked_list_of_specific_concern_objects:
                            if ranked_specific_concern_entry in related_specific_concern_qset:
                                related_specific_concern_qset = related_specific_concern_qset.exclude(
                                    question=ranked_specific_concern_entry.question)

                        no_of_specific_concerns_to_get = calculate_number_of_specific_concerns_to_fill(
                            no_of_gen_concern_objects, remaining_specific_concern_spots)

                        for specific_concern in related_specific_concern_qset:
                            if len(ranked_list_of_specific_concern_objects) < min_no_of_specific_concerns_to_fetch:
                                ranked_list_of_specific_concern_objects.append(specific_concern)

                                no_of_specific_concerns_to_get -= 1
                                if no_of_specific_concerns_to_get <= 0:
                                    break
                            else:
                                break

                        compile_ranked_list_of_specific_concern_objects(ordered_list_of_spec_conc_qsets[1:])

                return remaining_specific_concern_spots

            no_of_remaining_specific_concern_spots = compile_ranked_list_of_specific_concern_objects(
                list_of_related_specific_concern_qsets)
            while no_of_remaining_specific_concern_spots > 0:
                no_of_remaining_specific_concern_spots = compile_ranked_list_of_specific_concern_objects(
                    list_of_related_specific_concern_qsets)

            def parse_ranked_specific_concern_objects_and_add_data_to_response():
                response_data_entry = []
                for specific_concern in ranked_list_of_specific_concern_objects:
                    response_data_entry.append(specific_concern.return_values_dict())
                response_raw_data["Data"] = response_data_entry

            parse_ranked_specific_concern_objects_and_add_data_to_response()

    parse_POST_request_and_add_response = ranked_specific_concerns_post_logic
