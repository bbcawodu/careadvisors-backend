def filter_qset_by_full_name(qset, rqst_full_name):
    qset = qset.filter(full_name__iexact=rqst_full_name).order_by("full_name")

    return qset


def filter_qset_by_company_name(qset, rqst_company_name):
    qset = qset.filter(company_name__iexact=rqst_company_name).order_by("company_name")

    return qset


def filter_qset_by_email(qset, rqst_email):
    qset = qset.filter(email__iexact=rqst_email).order_by("email")

    return qset


def filter_qset_by_phone_number(qset, rqst_phone_number):
    qset = qset.filter(phone_number__iexact=rqst_phone_number).order_by("phone_number")

    return qset
