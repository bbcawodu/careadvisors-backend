from picmodels.models import ProviderLocation


def retrieve_id_plans(response_raw_data, rqst_errors, plans, rqst_plan_id, list_of_ids, include_summary_report=False, include_detailed_report=False):
    if rqst_plan_id == "all":
        all_plans = plans
        plan_dict = {}
        for plan in all_plans:
            plan_dict[plan.id] = plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report)
        plan_list = []
        for plan_key, plan_entry in plan_dict.items():
            plan_list.append(plan_entry)

        response_raw_data["Data"] = plan_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            plans = plans.filter(id__in=list_of_ids)
            if len(plans) > 0:

                plan_dict = {}
                for plan in plans:
                    plan_dict[plan.id] = plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report)
                plan_list = []
                for plan_key, plan_entry in plan_dict.items():
                    plan_list.append(plan_entry)
                response_raw_data["Data"] = plan_list

                for plan_id in list_of_ids:
                    if plan_id not in plan_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Plan with id: {!s} not found in database'.format(str(plan_id)))
            else:
                rqst_errors.append('No plans found for database ID(s): ' + rqst_plan_id)
        else:
            rqst_errors.append('No valid plan IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_name_plans(response_raw_data, rqst_errors, plans, rqst_name, include_summary_report=False, include_detailed_report=False):
    plans_list = []
    plans = plans.filter(name__iexact=rqst_name)

    if plans:
        for plan in plans:
            plans_list.append(plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report))
        response_raw_data["Data"] = plans_list
    else:
        rqst_errors.append('No plans with name: {!s} not found in database'.format(rqst_name))

    return response_raw_data, rqst_errors


def retrieve_plans_by_carrier_id(response_raw_data, rqst_errors, plans, rqst_carrier_id, list_of_carrier_ids, include_summary_report=False, include_detailed_report=False):
    if rqst_carrier_id == "all":
        all_plans = plans
        plan_dict = {}
        for plan in all_plans:
            plan_dict[plan.id] = plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report)
        plan_list = []
        for plan_key, plan_entry in plan_dict.items():
            plan_list.append(plan_entry)

        response_raw_data["Data"] = plan_list
    elif list_of_carrier_ids:
        if len(list_of_carrier_ids) > 0:
            for indx, element in enumerate(list_of_carrier_ids):
                list_of_carrier_ids[indx] = int(element)
            plans = plans.filter(carrier__id__in=list_of_carrier_ids)
            if len(plans) > 0:

                plan_dict = {}
                for plan in plans:
                    if plan.carrier.id not in plan_dict:
                        plan_dict[plan.carrier.id] = [plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report)]
                    else:
                        plan_dict[plan.carrier.id].append(plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report))
                plan_list = []
                for plan_key, plan_entry in plan_dict.items():
                    plan_list.append(plan_entry)
                response_raw_data["Data"] = plan_list

                for carrier_id in list_of_carrier_ids:
                    if carrier_id not in plan_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Plan with carrier id: {!s} not found in database'.format(str(carrier_id)))
            else:
                rqst_errors.append('No plans found for carrier database ID(s): ' + rqst_carrier_id)
        else:
            rqst_errors.append('No valid carrier database IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_plans_by_carrier_state(response_raw_data, rqst_errors, plans, rqst_carrier_state, list_of_carrier_states, include_summary_report=False, include_detailed_report=False):
    plans_dict = {}
    plans_object = plans
    for state in list_of_carrier_states:
        plans = plans_object.filter(carrier__state_province__iexact=state)
        for plan in plans:
            if state not in plans_dict:
                plans_dict[state] = [plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report)]
            else:
                plans_dict[state].append(plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report))
    if len(plans_dict) > 0:
        plans_list = []
        for plan_key, plan_entry in plans_dict.items():
            plans_list.append(plan_entry)
        response_raw_data["Data"] = plans_list
        for state in list_of_carrier_states:
            if state not in plans_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('No plans with a carrier in state: {!s} found in database'.format(state))
    else:
        rqst_errors.append('No plans with a carrier in state(s): {!s} found in database'.format(rqst_carrier_state))

    return response_raw_data, rqst_errors


def retrieve_plans_by_carrier_name(response_raw_data, rqst_errors, plans, rqst_carrier_name, include_summary_report=False, include_detailed_report=False):
    plans_list = []
    plans = plans.filter(carrier__name__iexact=rqst_carrier_name)

    if plans:
        for plan in plans:
            plans_list.append(plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report))
        response_raw_data["Data"] = plans_list
    else:
        rqst_errors.append('No Plans with a carrier with the name: {!s} found in database'.format(rqst_carrier_name))

    return response_raw_data, rqst_errors


def retrieve_plans_by_accepted_location_id(response_raw_data, rqst_errors, plans, rqst_accepted_location_id, list_of_accepted_location_ids, include_summary_report=False, include_detailed_report=False):
    if rqst_accepted_location_id == "all":
        all_plans = plans
        plan_dict = {}
        for plan in all_plans:
            plan_dict[plan.id] = plan.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report)
        plan_list = []
        for plan_key, plan_entry in plan_dict.items():
            plan_list.append(plan_entry)

        response_raw_data["Data"] = plan_list
    elif list_of_accepted_location_ids:
        if len(list_of_accepted_location_ids) > 0:

            for indx, element in enumerate(list_of_accepted_location_ids):
                integer_id = int(element)
                list_of_accepted_location_ids[indx] = integer_id

            provider_locations = ProviderLocation.objects.all().filter(id__in=list_of_accepted_location_ids)
            if provider_locations.count():
                plan_dict = {}

                for location_object in provider_locations:
                    location_id = location_object.id

                    accepted_plan_objects = location_object.accepted_plans.all()
                    if accepted_plan_objects.count():
                        for accepted_plan_object in accepted_plan_objects:
                            if location_id in plan_dict:
                                plan_dict[location_id].append(accepted_plan_object.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report))
                            else:
                                plan_dict[location_id] = [accepted_plan_object.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report)]
                    else:
                        plan_dict[location_id] = []

                plan_list = []
                for plan_key, plan_entry in plan_dict.items():
                    if plan_entry:
                        plan_list.append(plan_entry)
                response_raw_data["Data"] = plan_list

                for accepted_location_id in list_of_accepted_location_ids:
                    if accepted_location_id in plan_dict:
                        if not plan_dict[accepted_location_id]:
                            if response_raw_data['Status']['Error Code'] != 2:
                                response_raw_data['Status']['Error Code'] = 2
                            rqst_errors.append('Provider location with id: {!s} has no accepted plans'.format(str(accepted_location_id)))
                    else:
                        rqst_errors.append("No provider location found for id: {}".format(accepted_location_id))
            else:
                rqst_errors.append('No provider locations found for database ID(s): ' + rqst_accepted_location_id)

        else:
            rqst_errors.append('No valid provider location database IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors
