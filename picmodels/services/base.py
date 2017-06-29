def filter_db_queryset_by_id(db_queryset, rqst_id, list_of_ids):
    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.all()
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids)

    return db_queryset
