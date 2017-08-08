def filter_plan_qset_by_name(plan_qset, rqst_name):
    plan_qset = plan_qset.filter(name__iexact=rqst_name).order_by("name")

    return plan_qset


def filter_plan_qset_by_carrier_name(plan_qset, rqst_carrier_name):
    plan_qset = plan_qset.filter(carrier__name__iexact=rqst_carrier_name).order_by("id")

    return plan_qset
