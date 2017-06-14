def retrieve_id_carriers(response_raw_data, rqst_errors, carriers, rqst_carrier_id, list_of_ids):
    """
    This function takes a list of ids and a QueryList of HealthcareCarrier instances as parameters,
    filters the database with the parameters, and adds the carrier info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param carriers: (type: QueryList) QueryList of carriers
    :param rqst_carrier_id: (type: integer) carrier id
    :param list_of_ids: (type: list) list of carrier ids
    :return: (type: dictionary and list) response data and list of error messages
    """

    if rqst_carrier_id == "all":
        all_carriers = carriers
        carrier_dict = {}
        for carrier in all_carriers:
            carrier_dict[carrier.id] = carrier.return_values_dict()
        carrier_list = []
        for carrier_key, carrier_entry in carrier_dict.items():
            carrier_list.append(carrier_entry)

        response_raw_data["Data"] = carrier_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            carriers = carriers.filter(id__in=list_of_ids)
            if len(carriers) > 0:

                carrier_dict = {}
                for carrier in carriers:
                    carrier_dict[carrier.id] = carrier.return_values_dict()
                carrier_list = []
                for carrier_key, carrier_entry in carrier_dict.items():
                    carrier_list.append(carrier_entry)
                response_raw_data["Data"] = carrier_list

                for carrier_id in list_of_ids:
                    if carrier_id not in carrier_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Carrier with id: {!s} not found in database'.format(str(carrier_id)))
            else:
                rqst_errors.append('No carriers found for database ID(s): ' + rqst_carrier_id)
        else:
            rqst_errors.append('No valid carrier IDs provided in request (must be integers)')


def retrieve_state_carriers(response_raw_data, rqst_errors, carriers, rqst_state, list_of_states):
    carrier_dict = {}
    for state in list_of_states:
        name_carriers = carriers.filter(state_province__iexact=state)
        for carrier in name_carriers:
            if state not in carrier_dict:
                carrier_dict[state] = [carrier.return_values_dict()]
            else:
                carrier_dict[state].append(carrier.return_values_dict())
    if len(carrier_dict) > 0:
        carrier_list = []
        for carrier_key, carrier_entry in carrier_dict.items():
            carrier_list.append(carrier_entry)
        response_raw_data["Data"] = carrier_list
        for state in list_of_states:
            if state not in carrier_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Carriers in the state: {!s} not found in database'.format(state))
    else:
        rqst_errors.append('Carriers in the state(s): {!s} not found in database'.format(rqst_state))


def retrieve_name_carriers(response_raw_data, rqst_errors, carriers, rqst_name):
    """
    This function takes a carrier name and a QueryList of HealthcareCarrier instances as parameters,
    filters the database with the parameters, and adds the carrier info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param carriers: (type: QueryList) QueryList of consumers
    :param rqst_name: (type: string) consumer last name
    :return: (type: dictionary and list) response data and list of error messages
    """

    carrier_list = []
    carriers = carriers.filter(name__iexact=rqst_name)

    if carriers:
        if len(carriers) > 1:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Multiple carriers found in db for name: {!s}'.format(rqst_name))

        for carrier in carriers:
            carrier_list.append(carrier.return_values_dict())
        response_raw_data["Data"] = carrier_list
    else:
        rqst_errors.append('Carrier with name: {!s} not found in database'.format(rqst_name))


# def retrieve_name_carriers(response_raw_data, rqst_errors, carriers, rqst_name, list_of_names):
#     """
#     This function takes a carrier name and a QueryList of HealthcareCarrier instances as parameters,
#     filters the database with the parameters, and adds the carrier info the given dictionary of response data
#
#     :param response_raw_data: (type: dictionary) response data
#     :param rqst_errors: (type: list) list of error messages
#     :param carriers: (type: QueryList) QueryList of consumers
#     :param rqst_name: (type: string) consumer last name
#     :return: (type: dictionary and list) response data and list of error messages
#     """
#
#     carrier_list = []
#     carriers = carriers.filter(name__iexact=rqst_name)
#
#     if carriers:
#         if len(carriers) > 1:
#             if response_raw_data['Status']['Error Code'] != 2:
#                 response_raw_data['Status']['Error Code'] = 2
#             rqst_errors.append('Multiple carriers found in db for name: {!s}'.format(rqst_name))
#
#         for carrier in carriers:
#             carrier_list.append(carrier.return_values_dict())
#         response_raw_data["Data"] = carrier_list
#     else:
#         rqst_errors.append('Carrier with name: {!s} not found in database'.format(rqst_name))
#
#     return response_raw_data, rqst_errors
