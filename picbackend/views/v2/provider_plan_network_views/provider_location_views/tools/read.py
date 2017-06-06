def retrieve_provider_locations_by_id(response_raw_data, rqst_errors, provider_locations, rqst_provider_location_id, list_of_ids):
    if rqst_provider_location_id == "all":
        all_provider_locations = provider_locations
        provider_locations_dict = {}
        for provider_location in all_provider_locations:
            provider_locations_dict[provider_location.id] = provider_location.return_values_dict()
        provider_locations_list = []
        for provider_location_key, provider_location_entry in provider_locations_dict.items():
            provider_locations_list.append(provider_location_entry)

        response_raw_data["Data"] = provider_locations_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            provider_locations = provider_locations.filter(id__in=list_of_ids)
            if len(provider_locations) > 0:

                provider_locations_dict = {}
                for provider_location in provider_locations:
                    provider_locations_dict[provider_location.id] = provider_location.return_values_dict()
                provider_locations_list = []
                for provider_location_key, provider_location_entry in provider_locations_dict.items():
                    provider_locations_list.append(provider_location_entry)
                response_raw_data["Data"] = provider_locations_list

                for provider_location_id in list_of_ids:
                    if provider_location_id not in provider_locations_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Provider location with id: {!s} not found in database'.format(str(provider_location_id)))
            else:
                rqst_errors.append('No provider locations found for database ID(s): ' + rqst_provider_location_id)
        else:
            rqst_errors.append('No valid provider location IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_provider_locations_by_name(response_raw_data, rqst_errors, provider_locations, rqst_name):
    provider_locations_list = []
    provider_locations = provider_locations.filter(name__iexact=rqst_name)

    if provider_locations:
        for provider_location in provider_locations:
            provider_locations_list.append(provider_location.return_values_dict())
        response_raw_data["Data"] = provider_locations_list
    else:
        rqst_errors.append('No provider locations with name: {!s} not found in database'.format(rqst_name))

    return response_raw_data, rqst_errors


def retrieve_provider_locations_by_network_name(response_raw_data, rqst_errors, provider_locations, rqst_network_name):
    provider_locations_list = []
    provider_locations = provider_locations.filter(provider_network__name__iexact=rqst_network_name)

    if provider_locations:
        for provider_location in provider_locations:
            provider_locations_list.append(provider_location.return_values_dict())
        response_raw_data["Data"] = provider_locations_list
    else:
        rqst_errors.append('No provider locations with a provider network with the name: {!s} found in database'.format(rqst_network_name))

    return response_raw_data, rqst_errors


def retrieve_provider_locations_by_network_id(response_raw_data, rqst_errors, provider_locations, rqst_network_id, list_of_network_ids):
    if rqst_network_id == "all":
        all_provider_locations = provider_locations
        provider_locations_dict = {}
        for provider_location in all_provider_locations:
            provider_locations_dict[provider_location.id] = provider_location.return_values_dict()
        provider_locations_list = []
        for provider_location_key, provider_location_entry in provider_locations_dict.items():
            provider_locations_list.append(provider_location_entry)

        response_raw_data["Data"] = provider_locations_list
    elif list_of_network_ids:
        if len(list_of_network_ids) > 0:
            for indx, element in enumerate(list_of_network_ids):
                list_of_network_ids[indx] = int(element)
            provider_locations = provider_locations.filter(provider_network__id__in=list_of_network_ids)
            if len(provider_locations) > 0:

                provider_locations_dict = {}
                for provider_location in provider_locations:
                    if provider_location.provider_network.id not in provider_locations_dict:
                        provider_locations_dict[provider_location.provider_network.id] = [provider_location.return_values_dict()]
                    else:
                        provider_locations_dict[provider_location.provider_network.id].append(provider_location.return_values_dict())
                provider_locations_list = []
                for provider_location_key, provider_location_entry in provider_locations_dict.items():
                    provider_locations_list.append(provider_location_entry)
                response_raw_data["Data"] = provider_locations_list

                for network_id in list_of_network_ids:
                    if network_id not in provider_locations_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Provider location with provider network id: {!s} not found in database'.format(str(network_id)))
            else:
                rqst_errors.append('No provider locations found for provider network database ID(s): ' + rqst_network_id)
        else:
            rqst_errors.append('No valid provider network database IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors
