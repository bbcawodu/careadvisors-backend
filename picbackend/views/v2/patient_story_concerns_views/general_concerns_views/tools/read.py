def retrieve_general_concerns_by_id(response_raw_data, rqst_errors, general_concerns, rqst_general_concerns_id, list_of_ids):
    if rqst_general_concerns_id == "all":
        all_general_concerns = general_concerns
        general_concerns_dict = {}
        for general_concern in all_general_concerns:
            general_concerns_dict[general_concern.id] = general_concern.return_values_dict()
        general_concerns_list = []
        for general_concern_key, general_concern_entry in general_concerns_dict.items():
            general_concerns_list.append(general_concern_entry)

        response_raw_data["Data"] = general_concerns_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            general_concerns = general_concerns.filter(id__in=list_of_ids)
            if len(general_concerns) > 0:

                general_concerns_dict = {}
                for general_concern in general_concerns:
                    general_concerns_dict[general_concern.id] = general_concern.return_values_dict()
                general_concerns_list = []
                for general_concern_key, general_concern_entry in general_concerns_dict.items():
                    general_concerns_list.append(general_concern_entry)
                response_raw_data["Data"] = general_concerns_list

                for general_concern_id in list_of_ids:
                    if general_concern_id not in general_concerns_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('General concern with id: {!s} not found in database'.format(str(general_concern_id)))
            else:
                rqst_errors.append('No general concerns found for database ID(s): ' + rqst_general_concerns_id)
        else:
            rqst_errors.append('No valid general concern IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_general_concerns_by_name(response_raw_data, rqst_errors, general_concerns, rqst_name):
    general_concerns_list = []
    general_concerns = general_concerns.filter(name__iexact=rqst_name)

    if general_concerns:
        if len(general_concerns) > 1:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Multiple general concerns found in db for name: {!s}'.format(rqst_name))

        for general_concern in general_concerns:
            general_concerns_list.append(general_concern.return_values_dict())
        response_raw_data["Data"] = general_concerns_list
    else:
        rqst_errors.append('General concern with name: {!s} not found in database'.format(rqst_name))

    return response_raw_data, rqst_errors
