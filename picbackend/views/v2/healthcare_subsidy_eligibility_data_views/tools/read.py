def retrieve_healthcare_subsidy_eligibility_data_by_id(response_raw_data, rqst_errors, healthcare_subsidy_eligibility_data_objs, rqst_healthcare_subsidy_eligibility_data_id, list_of_ids):
    if rqst_healthcare_subsidy_eligibility_data_id == "all":
        all_healthcare_subsidy_eligibility_data_objs = healthcare_subsidy_eligibility_data_objs.all()
        healthcare_subsidy_eligibility_data_dict = {}
        for healthcare_subsidy_eligibility_data_instance in all_healthcare_subsidy_eligibility_data_objs:
            healthcare_subsidy_eligibility_data_dict[healthcare_subsidy_eligibility_data_instance.id] = healthcare_subsidy_eligibility_data_instance.return_values_dict()
        healthcare_subsidy_eligibility_data_list = []
        for healthcare_subsidy_eligibility_data_key, healthcare_subsidy_eligibility_data_entry in healthcare_subsidy_eligibility_data_dict.items():
            healthcare_subsidy_eligibility_data_list.append(healthcare_subsidy_eligibility_data_entry)

        response_raw_data["Data"] = healthcare_subsidy_eligibility_data_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            healthcare_subsidy_eligibility_data_objs = healthcare_subsidy_eligibility_data_objs.filter(id__in=list_of_ids)
            if len(healthcare_subsidy_eligibility_data_objs) > 0:
                healthcare_subsidy_eligibility_data_dict = {}
                for healthcare_subsidy_eligibility_data_instance in healthcare_subsidy_eligibility_data_objs:
                    healthcare_subsidy_eligibility_data_dict[healthcare_subsidy_eligibility_data_instance.id] = healthcare_subsidy_eligibility_data_instance.return_values_dict()
                healthcare_subsidy_eligibility_data_list = []
                for healthcare_subsidy_eligibility_data_key, healthcare_subsidy_eligibility_data_entry in healthcare_subsidy_eligibility_data_dict.items():
                    healthcare_subsidy_eligibility_data_list.append(healthcare_subsidy_eligibility_data_entry)
                response_raw_data["Data"] = healthcare_subsidy_eligibility_data_list

                for healthcare_subsidy_eligibility_data_id in list_of_ids:
                    if healthcare_subsidy_eligibility_data_id not in healthcare_subsidy_eligibility_data_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Healthcare subsidy eligibility data instance with id: {} not found in database'.format(healthcare_subsidy_eligibility_data_id))
            else:
                rqst_errors.append('No healthcare subsidy eligibility data instances found for database ID(s): ' + rqst_healthcare_subsidy_eligibility_data_id)
        else:
            rqst_errors.append('No valid healthcare subsidy eligibility data instance data IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_healthcare_subsidy_eligibility_data_by_family_size(response_raw_data, rqst_errors, healthcare_subsidy_eligibility_data_objs, rqst_family_size, list_of_family_sizes):
    if list_of_family_sizes:
        if len(list_of_family_sizes) > 0:
            healthcare_subsidy_eligibility_data_objs = healthcare_subsidy_eligibility_data_objs.filter(family_size__in=list_of_family_sizes)
            if len(healthcare_subsidy_eligibility_data_objs) > 0:
                healthcare_subsidy_eligibility_data_dict = {}
                for healthcare_subsidy_eligibility_data_instance in healthcare_subsidy_eligibility_data_objs:
                    healthcare_subsidy_eligibility_data_dict[healthcare_subsidy_eligibility_data_instance.family_size] = healthcare_subsidy_eligibility_data_instance.return_values_dict()
                healthcare_subsidy_eligibility_data_list = []
                for healthcare_subsidy_eligibility_data_key, healthcare_subsidy_eligibility_data_entry in healthcare_subsidy_eligibility_data_dict.items():
                    healthcare_subsidy_eligibility_data_list.append(healthcare_subsidy_eligibility_data_entry)
                response_raw_data["Data"] = healthcare_subsidy_eligibility_data_list

                for family_size in list_of_family_sizes:
                    if family_size not in healthcare_subsidy_eligibility_data_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Healthcare subsidy eligibility data instance with family size: {} not found in database'.format(family_size))
            else:
                rqst_errors.append(
                    'No healthcare subsidy eligibility data instances found for family size(s): ' + rqst_family_size)
        else:
            rqst_errors.append('No valid family sizes provided in request (must be integers)')

    return response_raw_data, rqst_errors
