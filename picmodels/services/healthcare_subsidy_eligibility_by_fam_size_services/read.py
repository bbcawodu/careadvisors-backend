def filter_healthcare_subsidy_eligibility_data_instances_by_id(healthcare_subsidy_eligibility_data_objs, rqst_healthcare_subsidy_eligibility_data_id, list_of_ids):
    if rqst_healthcare_subsidy_eligibility_data_id == "all":
        healthcare_subsidy_eligibility_data_objs = healthcare_subsidy_eligibility_data_objs.all()
    else:
        healthcare_subsidy_eligibility_data_objs = healthcare_subsidy_eligibility_data_objs.filter(id__in=list_of_ids)

    return healthcare_subsidy_eligibility_data_objs


def filter_healthcare_subsidy_eligibility_data_instances_by_family_size(healthcare_subsidy_eligibility_data_objs, list_of_family_sizes):
    healthcare_subsidy_eligibility_data_objs = healthcare_subsidy_eligibility_data_objs.filter(family_size__in=list_of_family_sizes)

    return healthcare_subsidy_eligibility_data_objs
