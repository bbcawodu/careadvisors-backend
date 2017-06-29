def filter_staff_objs_by_f_and_l_name(staff_objs, rqst_first_name, rqst_last_name):
    staff_objs = staff_objs.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)

    return staff_objs


def filter_staff_objs_by_first_name(staff_objs, rqst_first_name):
    staff_objs = staff_objs.filter(first_name__iexact=rqst_first_name)

    return staff_objs


def filter_staff_objs_by_last_name(staff_objs, rqst_last_name):
    staff_objs = staff_objs.filter(last_name__iexact=rqst_last_name)

    return staff_objs


def filter_staff_objs_by_email(staff_objs, rqst_email):
    staff_objs = staff_objs.filter(email__iexact=rqst_email)

    return staff_objs


def filter_staff_objs_by_mpn(staff_objs, rqst_mpn):
    staff_objs = staff_objs.filter(mpn__iexact=rqst_mpn)

    return staff_objs
