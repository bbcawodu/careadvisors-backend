"""
Defines utility functions and classes for consumer views
"""


import math


def retrieve_f_l_name_consumers(response_raw_data, rqst_errors, consumers, rqst_first_name, rqst_last_name):
    """
    This function takes first and last name consumer parameters as well as a QueryList of PICConsumer instances,
    filters the database with the parameters, and adds the consumer info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param consumers: (type: QueryList) QueryList of consumers
    :param rqst_first_name: (type: string) consumer first name
    :param rqst_last_name: (type: string) consumer last name
    :return: (type: dictionary and list) response data and list of error messages
    """

    consumers = consumers.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)
    if len(consumers) > 0:
        consumer_dict = {}
        rqst_full_name = rqst_first_name + " " + rqst_last_name
        for consumer in consumers:
            if rqst_full_name not in consumer_dict:
                consumer_dict[rqst_full_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[rqst_full_name].append(consumer.return_values_dict())

        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
    else:
        rqst_errors.append('Consumer with name: {!s} {!s} not found in database'.format(rqst_first_name,
                                                                                            rqst_last_name))


def retrieve_email_consumers(response_raw_data, rqst_errors, consumers, rqst_email, list_of_emails):
    """
    This function takes an email consumer parameter and a QueryList of PICConsumer instances,
    filters the database with the parameters, and adds the consumer info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param consumers: (type: QueryList) QueryList of consumers
    :param rqst_email: (type: string) consumer email
    :param list_of_emails: (type: list) list of consumer emails
    :return: (type: dictionary and list) response data and list of error messages
    """

    consumer_dict = {}
    consumers_object = consumers
    for email in list_of_emails:
        consumers = consumers_object.filter(email__iexact=email)
        for consumer in consumers:
            if email not in consumer_dict:
                consumer_dict[email] = [consumer.return_values_dict()]
            else:
                consumer_dict[email].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for email in list_of_emails:
            if email not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Consumer with email: {!s} not found in database'.format(email))
    else:
        rqst_errors.append('Consumer with emails(s): {!s} not found in database'.format(rqst_email))


def retrieve_first_name_consumers(response_raw_data, rqst_errors, consumers, rqst_first_name, list_of_first_names):
    """
    This function takes a first name consumer parameter and a QueryList of PICConsumer instances,
    filters the database with the parameters, and adds the consumer info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param consumers: (type: QueryList) QueryList of consumers
    :param rqst_first_name: (type: string) consumer first name
    :param list_of_first_names: (type: list) list of consumer first names
    :return: (type: dictionary and list) response data and list of error messages
    """

    consumer_dict = {}
    consumers_object = consumers
    for first_name in list_of_first_names:
        consumers = consumers_object.filter(first_name__iexact=first_name)
        for consumer in consumers:
            if first_name not in consumer_dict:
                consumer_dict[first_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[first_name].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for name in list_of_first_names:
            if name not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Consumer with first name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Consumer with first name(s): {!s} not found in database'.format(rqst_first_name))


def retrieve_last_name_consumers(response_raw_data, rqst_errors, consumers, rqst_last_name, list_of_last_names):
    """
    This function takes a last name consumer parameter and a QueryList of PICConsumer instances,
    filters the database with the parameters, and adds the consumer info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param consumers: (type: QueryList) QueryList of consumers
    :param rqst_last_name: (type: string) consumer last name
    :param list_of_last_names: (type: list) list of consumer last names
    :return: (type: dictionary and list) response data and list of error messages
    """

    consumer_dict = {}
    consumers_object = consumers
    for last_name in list_of_last_names:
        consumers = consumers_object.filter(last_name__iexact=last_name)
        for consumer in consumers:
            if last_name not in consumer_dict:
                consumer_dict[last_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[last_name].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for name in list_of_last_names:
            if name not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member with last name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Staff Member with last name(s): {!s} not found in database'.format(rqst_last_name))


def retrieve_id_consumers(response_raw_data, rqst_errors, consumers, rqst_consumer_id, list_of_ids):
    """
    This function takes an id consumer parameter and a QueryList of PICConsumer instances,
    filters the database with the parameters, and adds the consumer info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param consumers: (type: QueryList) QueryList of consumers
    :param rqst_consumer_id: (type: integer) consumer id
    :param list_of_ids: (type: list) list of consumer ids
    :return: (type: dictionary and list) response data and list of error messages
    """

    if rqst_consumer_id == "all":
        all_consumers = consumers
        consumer_dict = {}
        for consumer in all_consumers:
            consumer_dict[consumer.id] = consumer.return_values_dict()
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)

        response_raw_data["Data"] = consumer_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            consumers = consumers.filter(id__in=list_of_ids)
            if len(consumers) > 0:

                consumer_dict = {}
                for consumer in consumers:
                    consumer_dict[consumer.id] = consumer.return_values_dict()
                consumer_list = []
                for consumer_key, consumer_entry in consumer_dict.items():
                    consumer_list.append(consumer_entry)
                response_raw_data["Data"] = consumer_list

                for consumer_id in list_of_ids:
                    if consumer_id not in consumer_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Consumer with id: {!s} not found in database'.format(str(consumer_id)))
            else:
                rqst_errors.append('No consumers found for database ID(s): ' + rqst_consumer_id)
        else:
            rqst_errors.append('No valid consumer IDs provided in request (must be integers)')


def break_results_into_pages(response_raw_data, CONSUMERS_PER_PAGE, rqst_page_no, base_url):
    """
    This function takes a dictionary of response data for a PIC Consumer GET API request, replaces excess consumer info
    with ids, and adds a key value pair of urls for subsequent pages of full PIC consumer info

    :param request: (type: Django request object) current request
    :param response_raw_data: (type: dictionary) response data
    :param CONSUMERS_PER_PAGE: (type: integer) number of full consumer info entries per page
    :param rqst_page_no: (type: integer) current page number
    :return: (type: dictionary) response data
    """

    consumer_list = response_raw_data["Data"]

    if len(consumer_list) > CONSUMERS_PER_PAGE:
        page_urls = []

        if rqst_page_no:
            if len(consumer_list) > ((rqst_page_no - 1) * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[:(CONSUMERS_PER_PAGE * (rqst_page_no - 1))]):
                    consumer_list[i] = consumer["Database ID"]
            if len(consumer_list) > (rqst_page_no * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE):]):
                    consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE)+i] = consumer["Database ID"]
        else:
            total_pages = math.ceil(len(consumer_list) / CONSUMERS_PER_PAGE)
            for i in range(total_pages):
                page_urls.append(base_url + "&page=" + str(i+1))

            for i, consumer in enumerate(consumer_list[CONSUMERS_PER_PAGE:]):
                consumer_list[CONSUMERS_PER_PAGE+i] = consumer["Database ID"]

        if page_urls:
            response_raw_data['Page URLs'] = page_urls

    response_raw_data["Data"] = consumer_list
