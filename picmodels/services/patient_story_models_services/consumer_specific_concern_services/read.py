def filter_specific_concern_objs_by_question(specific_concern_objs, rqst_question):
    specific_concern_objs = specific_concern_objs.filter(question__iexact=rqst_question)

    return specific_concern_objs


def filter_specific_concern_objs_by_gen_concern_name(specific_concern_objs, rqst_gen_concern_name):
    specific_concern_objs = specific_concern_objs.filter(related_general_concerns__name__iexact=rqst_gen_concern_name)

    return specific_concern_objs


def filter_specific_concern_objs_by_gen_concern_id(specific_concern_objs, list_of_gen_concern_ids):
    specific_concern_objs = specific_concern_objs.filter(id__in=list_of_gen_concern_ids)

    return specific_concern_objs


def filter_specific_concern_objs_by_gen_concern_id_subset(specific_concern_objs, list_of_gen_concern_ids):
    for gen_concern_id in list_of_gen_concern_ids:
        specific_concern_objs = specific_concern_objs.filter(related_general_concerns__id=gen_concern_id)

    return specific_concern_objs
