def filter_consumer_objs_by_f_and_l_name(consumer_objs, rqst_first_name, rqst_last_name):
    consumer_objs = consumer_objs.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)

    return consumer_objs


def filter_consumer_objs_by_email(consumer_objs, rqst_email):
    consumer_objs = consumer_objs.filter(email__iexact=rqst_email)

    return consumer_objs


def filter_consumer_objs_by_first_name(consumer_objs, rqst_first_name):
    consumer_objs = consumer_objs.filter(first_name__iexact=rqst_first_name)

    return consumer_objs


def filter_consumer_objs_by_last_name(consumer_objs, rqst_last_name):
    consumer_objs = consumer_objs.filter(last_name__iexact=rqst_last_name)

    return consumer_objs
