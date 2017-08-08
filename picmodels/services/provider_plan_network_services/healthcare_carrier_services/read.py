def filter_carrier_objs_by_state(carrier_qset, state):
    carrier_qset = carrier_qset.filter(state_province__iexact=state).order_by("state_province")

    return carrier_qset


def filter_carrier_objs_by_name(carrier_qset, name):
    carrier_qset = carrier_qset.filter(name__iexact=name).order_by("name")

    return carrier_qset
