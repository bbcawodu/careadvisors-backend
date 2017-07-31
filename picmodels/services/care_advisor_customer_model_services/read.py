def filter_qset_by_first_name_and_last_name(qset, rqst_first_name, rqst_last_name):
    qset = qset.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)

    return qset


def filter_qset_by_first_name(qset, rqst_first_name):
    qset = qset.filter(first_name__iexact=rqst_first_name)

    return qset


def filter_qset_by_last_name(qset, rqst_last_name):
    qset = qset.filter(last_name__iexact=rqst_last_name)

    return qset


def filter_qset_by_company_name(qset, rqst_company_name):
    qset = qset.filter(company_name__iexact=rqst_company_name)

    return qset


def filter_qset_by_email(qset, rqst_email):
    qset = qset.filter(email__iexact=rqst_email)

    return qset


def filter_qset_by_phone_number(qset, rqst_phone_number):
    qset = qset.filter(phone_number__iexact=rqst_phone_number)

    return qset
