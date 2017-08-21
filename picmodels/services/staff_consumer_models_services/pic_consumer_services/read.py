def filter_consumer_qset_by_id(db_queryset, rqst_id, list_of_ids):
    db_queryset = db_queryset.prefetch_related('consumernote_set',
                                               'address',
                                               'navigator',
                                               'cps_info__cps_location',
                                               'cps_info__primary_dependent',
                                               'cps_info__secondary_dependents')

    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_consumer_objs_by_f_and_l_name(consumer_objs, rqst_first_name, rqst_last_name):
    consumer_objs = consumer_objs.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name).order_by("last_name", "first_name")

    return consumer_objs


def filter_consumer_objs_by_email(consumer_objs, rqst_email):
    consumer_objs = consumer_objs.filter(email__iexact=rqst_email).order_by("email")

    return consumer_objs


def filter_consumer_objs_by_first_name(consumer_objs, rqst_first_name):
    consumer_objs = consumer_objs.filter(first_name__iexact=rqst_first_name).order_by("first_name")

    return consumer_objs


def filter_consumer_objs_by_last_name(consumer_objs, rqst_last_name):
    consumer_objs = consumer_objs.filter(last_name__iexact=rqst_last_name).order_by("last_name")

    return consumer_objs
