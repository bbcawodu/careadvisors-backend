from picmodels.models import ConsumerGeneralConcern


def retrieve_specific_concerns_by_id(response_raw_data, rqst_errors, specific_concerns, rqst_specific_concern_id, list_of_ids):
    if rqst_specific_concern_id == "all":
        all_specific_concerns = specific_concerns
        specific_concerns_dict = {}
        for specific_concern in all_specific_concerns:
            specific_concerns_dict[specific_concern.id] = specific_concern.return_values_dict()
        specific_concerns_list = []
        for specific_concern_key, specific_concern_entry in specific_concerns_dict.items():
            specific_concerns_list.append(specific_concern_entry)

        response_raw_data["Data"] = specific_concerns_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            specific_concerns = specific_concerns.filter(id__in=list_of_ids)
            if len(specific_concerns) > 0:
                specific_concerns_dict = {}
                for specific_concern in specific_concerns:
                    specific_concerns_dict[specific_concern.id] = specific_concern.return_values_dict()
                specific_concerns_list = []
                for specific_concern_key, specific_concern_entry in specific_concerns_dict.items():
                    specific_concerns_list.append(specific_concern_entry)
                response_raw_data["Data"] = specific_concerns_list

                for specific_concerns_id in list_of_ids:
                    if specific_concerns_id not in specific_concerns_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Specific concern with id: {!s} not found in database'.format(str(specific_concerns_id)))
            else:
                rqst_errors.append('No specific concerns found for database ID(s): ' + rqst_specific_concern_id)
        else:
            rqst_errors.append('No valid specific concern IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_specific_concerns_by_question(response_raw_data, rqst_errors, specific_concerns, rqst_question):
    specific_concerns_list = []
    specific_concerns = specific_concerns.filter(question__iexact=rqst_question)

    if specific_concerns:
        for specific_concern in specific_concerns:
            specific_concerns_list.append(specific_concern.return_values_dict())
        response_raw_data["Data"] = specific_concerns_list
    else:
        rqst_errors.append('No specific concern with question: {!s} found in database'.format(rqst_question))

    return response_raw_data, rqst_errors


def retrieve_specific_concerns_by_gen_concern_name(response_raw_data, rqst_errors, specific_concerns, rqst_gen_concern_name):
    specific_concerns_list = []
    specific_concerns = specific_concerns.filter(related_general_concerns__name__iexact=rqst_gen_concern_name)

    if specific_concerns:
        for specific_concern in specific_concerns:
            specific_concerns_list.append(specific_concern.return_values_dict())
        response_raw_data["Data"] = specific_concerns_list
    else:
        rqst_errors.append('No specific concerns whose related general concerns contain an entry with the name: {!s} found in database'.format(rqst_gen_concern_name))

    return response_raw_data, rqst_errors


def retrieve_specific_concerns_by_gen_concern_id_subset(response_raw_data, rqst_errors, specific_concerns, rqst_gen_concern_id, list_of_gen_concern_ids):
    if len(list_of_gen_concern_ids) > 0:
        for indx, element in enumerate(list_of_gen_concern_ids):
            list_of_gen_concern_ids[indx] = int(element)
        for gen_concern_id in list_of_gen_concern_ids:
            specific_concerns = specific_concerns.filter(related_general_concerns__id=gen_concern_id)
        if len(specific_concerns) > 0:
            specific_concerns_list = []
            for specific_concern in specific_concerns:
                specific_concerns_list.append(specific_concern.return_values_dict())

            response_raw_data["Data"] = specific_concerns_list
        else:
            rqst_errors.append('No specific concerns found for general concern database ID(s): ' + rqst_gen_concern_id)
    else:
        rqst_errors.append('No valid general concern database IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_specific_concerns_by_gen_concern_id(response_raw_data, rqst_errors, specific_concerns, rqst_gen_concern_id, list_of_gen_concern_ids):
    if len(list_of_gen_concern_ids) > 0:
        for indx, element in enumerate(list_of_gen_concern_ids):
            list_of_gen_concern_ids[indx] = int(element)
        general_concern_objs = ConsumerGeneralConcern.objects.all().filter(id__in=list_of_gen_concern_ids)
        if len(general_concern_objs) > 0:
            specific_concerns_dict = {}
            for gen_concern_obj in general_concern_objs:
                cur_specific_concern_qset = gen_concern_obj.related_specific_concerns.all()
                if len(cur_specific_concern_qset) > 0:
                    for specific_concern_object in cur_specific_concern_qset:
                        if gen_concern_obj.id not in specific_concerns_dict:
                            specific_concerns_dict[gen_concern_obj.id] = [specific_concern_object.return_values_dict()]
                        else:
                            specific_concerns_dict[gen_concern_obj.id].append(specific_concern_object.return_values_dict())

            for gen_concern_id in list_of_gen_concern_ids:
                if gen_concern_id not in specific_concerns_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('No specific concerns found whose related_general_concerns contain a general concern with database id: {}'.format(gen_concern_id))

            specific_concerns_list = []
            for gen_concern_key, specific_concerns_entry in specific_concerns_dict.items():
                specific_concerns_list.append(specific_concerns_entry)
            response_raw_data["Data"] = specific_concerns_list
        else:
            rqst_errors.append("No general concerns found in database for given database id(s): {}".format(rqst_gen_concern_id))
    else:
        rqst_errors.append('No valid general concern database IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors