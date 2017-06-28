def filter_provider_location_instances_by_name(provider_location_qset, rqst_name):
    provider_location_qset = provider_location_qset.filter(name__iexact=rqst_name)

    return provider_location_qset


def filter_provider_location_instances_by_provider_network_name(provider_location_qset, rqst_provider_network_name):
    provider_location_qset = provider_location_qset.filter(provider_network__name__iexact=rqst_provider_network_name)

    return provider_location_qset


def filter_provider_location_instances_by_provider_network_id(provider_location_qset, rqst_provider_network_id):
    provider_location_qset = provider_location_qset.filter(provider_network__id=rqst_provider_network_id)

    return provider_location_qset
