def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.select_related(
        'carrier',
    )

    db_queryset = db_queryset.prefetch_related(
        "primary_care_physician_standard_cost",
        "specialist_standard_cost",
        "emergency_room_standard_cost",
        "inpatient_facility_standard_cost",
        "generic_drugs_standard_cost",
        "preferred_brand_drugs_standard_cost",
        "non_preferred_brand_drugs_standard_cost",
        "specialty_drugs_standard_cost"
    )

    return db_queryset


def filter_plan_qset_by_id(db_queryset, rqst_id, list_of_ids):
    db_queryset = prefetch_related_rows(db_queryset)

    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_plan_qset_by_name(db_queryset, rqst_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(name__iexact=rqst_name).order_by("name")

    return db_queryset


def filter_plan_qset_by_carrier_name(db_queryset, rqst_carrier_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(carrier__name__iexact=rqst_carrier_name).order_by("id")

    return db_queryset
