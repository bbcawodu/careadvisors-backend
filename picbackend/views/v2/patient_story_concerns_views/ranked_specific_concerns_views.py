from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..utils import clean_list_value_from_dict_object
from picmodels.models import ConsumerGeneralConcern
from ..base import JSONPOSTRspMixin
from math import ceil


MAX_NO_OF_GEN_CONCERNS_GIVEN = 6
MIN_NO_OF_SPECIFIC_CONCERNS_TO_FETCH = 10


#Need to abstract common variables in get and post class methods into class attributes
class RankedSpecificConcernsView(JSONPOSTRspMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RankedSpecificConcernsView, self).dispatch(request, *args, **kwargs)

    def ranked_specific_concerns_post_logic(self, post_data, response_raw_data, post_errors):
        ranked_gen_concs_objects_w_rel_spec_concs, total_no_of_rel_spec_concerns = retrieve_ranked_gen_concern_entries_from_list_of_names(post_data, post_errors)
        if total_no_of_rel_spec_concerns == 0:
            post_errors.append("There are no related specific concern objects in the db for the given general concerns.")

        if not post_errors:
            if total_no_of_rel_spec_concerns < MIN_NO_OF_SPECIFIC_CONCERNS_TO_FETCH:
                min_no_of_specific_concerns_to_fetch = total_no_of_rel_spec_concerns
            else:
                min_no_of_specific_concerns_to_fetch = MIN_NO_OF_SPECIFIC_CONCERNS_TO_FETCH
            response_raw_data["min_entries"] = min_no_of_specific_concerns_to_fetch

            ranked_list_of_specific_concern_objects = []
            no_of_gen_concern_objects = len(ranked_gen_concs_objects_w_rel_spec_concs)

            def compile_ranked_list_of_specific_concern_objects():
                for indx, gen_concern_object_w_rel_spec_concs in enumerate(ranked_gen_concs_objects_w_rel_spec_concs):
                    related_specific_concerns = gen_concern_object_w_rel_spec_concs[1]
                    for ranked_specific_concern_entry in ranked_list_of_specific_concern_objects:
                        if ranked_specific_concern_entry in related_specific_concerns:
                            related_specific_concerns = related_specific_concerns.exclude(question=ranked_specific_concern_entry.question)

                    # need to write formula to obtain percentage from no_of_gen_concern_objects and index in list
                    percentage_of_specific_concerns_to_get = (1/no_of_gen_concern_objects) * \
                                                             1#<-formula to obtain percentage goes here
                    no_of_specific_concerns_to_get = ceil(percentage_of_specific_concerns_to_get * min_no_of_specific_concerns_to_fetch)

                    for specific_concern in related_specific_concerns:
                        ranked_list_of_specific_concern_objects.append(specific_concern)

                        no_of_specific_concerns_to_get -= 1
                        if no_of_specific_concerns_to_get <= 0:
                            break

                no_of_remaining_specific_concern_spots = min_no_of_specific_concerns_to_fetch - len(ranked_list_of_specific_concern_objects)
                return no_of_remaining_specific_concern_spots

            no_of_remaining_specific_concern_spots = compile_ranked_list_of_specific_concern_objects()
            while no_of_remaining_specific_concern_spots > 0:
                no_of_remaining_specific_concern_spots = compile_ranked_list_of_specific_concern_objects()

            response_data_entry = []
            for specific_concern in ranked_list_of_specific_concern_objects:
                response_data_entry.append(specific_concern.return_values_dict())
            response_raw_data["Data"] = response_data_entry

        return response_raw_data, post_errors

    post_logic_function = ranked_specific_concerns_post_logic


def retrieve_ranked_gen_concern_entries_from_list_of_names(rqst_data, rqst_errors):
    ranked_gen_concs_objects_w_rel_spec_concs = []
    total_related_spec_concerns_qset = None
    total_no_of_rel_spec_concerns = 0

    rqst_ranked_general_concerns_names = clean_list_value_from_dict_object(rqst_data, "root", "ranked_general_concerns",
                                                                           rqst_errors)
    if len(rqst_errors) == 0:
        no_of_ranked_gen_concerns = len(rqst_ranked_general_concerns_names)
        if no_of_ranked_gen_concerns <= MAX_NO_OF_GEN_CONCERNS_GIVEN:
            for indx, general_concern_name in enumerate(rqst_ranked_general_concerns_names):
                if not isinstance(general_concern_name, str):
                    rqst_errors.append(
                        "All ranked general concerns must be strings, ranked general concern is not an string for 'related_general_concerns' field at index: {}".format(
                            indx))

            ranked_general_concerns_names_set = set(rqst_ranked_general_concerns_names)
            if len(ranked_general_concerns_names_set) != len(rqst_ranked_general_concerns_names):
                rqst_errors.append("There are duplicates in the 'ranked_general_concerns' list. No duplicates allowed")

            if not rqst_errors:
                ranked_general_concerns_errors = []

                for ranked_general_concerns_name in rqst_ranked_general_concerns_names:
                    try:
                        ranked_general_concerns_object = ConsumerGeneralConcern.objects.get(
                            name__iexact=ranked_general_concerns_name)

                        related_spec_concerns_qset = ranked_general_concerns_object.related_specific_concerns.all().order_by("-research_weight")
                        if total_related_spec_concerns_qset:
                            total_related_spec_concerns_qset = total_related_spec_concerns_qset | related_spec_concerns_qset
                        else:
                            total_related_spec_concerns_qset = related_spec_concerns_qset

                        ranked_general_concerns_objects_entry = [ranked_general_concerns_object, related_spec_concerns_qset]
                        ranked_gen_concs_objects_w_rel_spec_concs.append(ranked_general_concerns_objects_entry)
                    except ConsumerGeneralConcern.DoesNotExist:
                        ranked_general_concerns_errors.append(
                            "No ConsumerGeneralConcern database entry found for name: {}".format(ranked_general_concerns_name))

                if total_related_spec_concerns_qset:
                    total_no_of_rel_spec_concerns = total_related_spec_concerns_qset.distinct().count()

                for ranked_general_concerns_error in ranked_general_concerns_errors:
                    rqst_errors.append(ranked_general_concerns_error)
        else:
            rqst_errors.append("Maximum number of ranked_general_concerns is {}, the number given is: {}".format(
                MAX_NO_OF_GEN_CONCERNS_GIVEN, no_of_ranked_gen_concerns))

    return ranked_gen_concs_objects_w_rel_spec_concs, total_no_of_rel_spec_concerns
