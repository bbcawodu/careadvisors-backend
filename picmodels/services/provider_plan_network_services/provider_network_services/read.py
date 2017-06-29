def filter_provider_network_instances_by_name(provider_network_qset, rqst_name):
    provider_network_qset = provider_network_qset.filter(name__iexact=rqst_name)

    return provider_network_qset
