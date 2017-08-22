def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.prefetch_related('consumernote_set',
                                               'address',
                                               'navigator',
                                               'cps_info__cps_location',
                                               'cps_info__primary_dependent',
                                               'cps_info__secondary_dependents')

    return db_queryset


def filter_consumer_qset_by_id(db_queryset, rqst_id, list_of_ids):
    db_queryset = prefetch_related_rows(db_queryset)

    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_consumer_objs_by_f_and_l_name(db_queryset, rqst_first_name, rqst_last_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name).order_by("last_name", "first_name")

    return db_queryset


def filter_consumer_objs_by_email(db_queryset, rqst_email):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(email__iexact=rqst_email).order_by("email")

    return db_queryset


def filter_consumer_objs_by_first_name(db_queryset, rqst_first_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(first_name__iexact=rqst_first_name).order_by("first_name")

    return db_queryset


def filter_consumer_objs_by_last_name(db_queryset, rqst_last_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(last_name__iexact=rqst_last_name).order_by("last_name")

    return db_queryset
