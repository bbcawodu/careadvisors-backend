def retrieve_provider_networks_by_id(response_raw_data, rqst_errors, provider_networks, rqst_provider_network_id, list_of_ids):
    if rqst_provider_network_id == "all":
        all_provider_networks = provider_networks
        provider_networks_dict = {}
        for provider_network in all_provider_networks:
            provider_networks_dict[provider_network.id] = provider_network.return_values_dict()
        provider_networks_list = []
        for provider_network_key, provider_network_entry in provider_networks_dict.items():
            provider_networks_list.append(provider_network_entry)

        response_raw_data["Data"] = provider_networks_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            provider_networks = provider_networks.filter(id__in=list_of_ids)
            if len(provider_networks) > 0:
                provider_networks_dict = {}
                for provider_network in provider_networks:
                    provider_networks_dict[provider_network.id] = provider_network.return_values_dict()
                provider_networks_list = []
                for provider_network_key, provider_network_entry in provider_networks_dict.items():
                    provider_networks_list.append(provider_network_entry)
                response_raw_data["Data"] = provider_networks_list

                for provider_network_id in list_of_ids:
                    if provider_network_id not in provider_networks_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Provider network with id: {!s} not found in database'.format(str(provider_network_id)))
            else:
                rqst_errors.append('No provider networks found for database ID(s): ' + rqst_provider_network_id)
        else:
            rqst_errors.append('No valid provider network IDs provided in request (must be integers)')


def retrieve_provider_networks_by_name(response_raw_data, rqst_errors, provider_networks, rqst_name):
    provider_networks_list = []
    provider_networks = provider_networks.filter(name__iexact=rqst_name)

    if provider_networks:
        for provider_network in provider_networks:
            provider_networks_list.append(provider_network.return_values_dict())
        response_raw_data["Data"] = provider_networks_list
    else:
        rqst_errors.append('No provider networks with name: {!s} not found in database'.format(rqst_name))
