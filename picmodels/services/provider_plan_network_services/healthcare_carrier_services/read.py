def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.prefetch_related('healthcareplan_set')

    return db_queryset


def filter_carrier_qset_by_id(db_queryset, rqst_id, list_of_ids):
    db_queryset = prefetch_related_rows(db_queryset)

    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_carrier_objs_by_state(db_queryset, state):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(state_province__iexact=state).order_by("state_province")

    return db_queryset


def filter_carrier_objs_by_name(db_queryset, name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(name__iexact=name).order_by("name")

    return db_queryset
