def filter_general_concern_objs_by_name(general_concern_objs, rqst_name):
    general_concern_objs = general_concern_objs.filter(name__iexact=rqst_name).order_by("name")

    return general_concern_objs
