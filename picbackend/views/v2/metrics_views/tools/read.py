"""
Defines utility functions and classes for consumer metrics views
"""

from picmodels.models import PICStaff


# defines function to group metrics by given parameter
def group_metrics_by_rqst_param(metrics_dict, grouping_parameter):
    return_dict = {}
    if grouping_parameter == "County":
        for staff_key, staff_dict in metrics_dict.items():
            for metrics_entry in staff_dict["Metrics Data"]:
                if metrics_entry[grouping_parameter] not in return_dict:
                    return_dict[metrics_entry[grouping_parameter]] = {staff_key: {"Metrics Data": [metrics_entry],
                                                                      "Staff Information": staff_dict["Staff Information"]}}
                else:
                    if staff_key not in return_dict[metrics_entry[grouping_parameter]]:
                        return_dict[metrics_entry[grouping_parameter]][staff_key] = {"Metrics Data": [metrics_entry],
                                                                                     "Staff Information": staff_dict["Staff Information"]}
                    else:
                        return_dict[metrics_entry[grouping_parameter]][staff_key]["Metrics Data"].append(metrics_entry)

    elif grouping_parameter == "Zipcode":
        for staff_key, staff_dict in metrics_dict.items():
            for metrics_entry in staff_dict["Metrics Data"]:
                if metrics_entry["Location"][grouping_parameter] not in return_dict:
                    return_dict[metrics_entry["Location"][grouping_parameter]] = {staff_key: {"Metrics Data": [metrics_entry],
                                                                      "Staff Information": staff_dict["Staff Information"]}}
                else:
                    if staff_key not in return_dict[metrics_entry["Location"][grouping_parameter]]:
                        return_dict[metrics_entry["Location"][grouping_parameter]][staff_key] = {"Metrics Data": [metrics_entry],
                                                                                     "Staff Information": staff_dict["Staff Information"]}
                    else:
                        return_dict[metrics_entry["Location"][grouping_parameter]][staff_key]["Metrics Data"].append(metrics_entry)
    return return_dict


def retrieve_id_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_id, list_of_ids, fields=None):
    if rqst_staff_id.lower() != "all":
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

    metrics_dict = {}
    if len(metrics_submissions) > 0:
        for metrics_submission in metrics_submissions:
            values_dict = metrics_submission.return_values_dict()
            filtered_values_dict = {}
            if fields:
                for field in fields:
                    filtered_values_dict[field] = values_dict[field]
            else:
                filtered_values_dict = values_dict

            if metrics_submission.staff_member_id not in metrics_dict:
                metrics_dict[metrics_submission.staff_member_id] = {"Metrics Data": [filtered_values_dict]}
                metrics_dict[metrics_submission.staff_member_id]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
            else:
                metrics_dict[metrics_submission.staff_member_id]["Metrics Data"].append(filtered_values_dict)

        if rqst_staff_id.lower() != "all":
            for staff_id in list_of_ids:
                if staff_id not in metrics_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Metrics for staff Member with id: {!s} not found in database'.format(str(staff_id)))
                    response_raw_data["Status"]["Missing Parameters"].append(str(staff_id))
    else:
        rqst_errors.append('No metrics entries for staff ID(s): {!s} not found in database'.format(rqst_staff_id))
        response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_id)

    return metrics_dict


def retrieve_f_l_name_metrics(response_raw_data, rqst_errors, metrics_submissions, list_of_first_names, list_of_last_names, rqst_fname, rqst_lname, fields=None):
    metrics_dict = {}
    if len(list_of_first_names) == len(list_of_last_names):
        list_of_ids = []
        for i, first_name in enumerate(list_of_first_names):
            last_name = list_of_last_names[i]
            name_ids = PICStaff.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).values_list('id', flat=True)
            if len(name_ids) > 0:
                list_of_ids.append(name_ids)
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Metrics for staff member with name: {!s} {!s} not found in database'.format(first_name, last_name))
                response_raw_data["Status"]["Missing Parameters"].append(first_name + last_name)
        list_of_ids = list(set().union(*list_of_ids))
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_fname + rqst_lname)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                staff_id = metrics_submission.staff_member.id
                staff_info_dict = metrics_submission.staff_member.return_values_dict()

                metrics_params_dict_entry = {
                    "Metrics Data": [filtered_values_dict],
                    "Staff Information": staff_info_dict
                }

                name = '{!s} {!s}'.format(metrics_submission.staff_member.first_name, metrics_submission.staff_member.last_name)
                if name not in metrics_dict:
                    metrics_dict[name] = {staff_id: metrics_params_dict_entry}
                else:
                    metrics_param_dict = metrics_dict[name]

                    if staff_id in metrics_param_dict:
                        metrics_param_dict[staff_id]["Metrics Data"].append(filtered_values_dict)
                    else:
                        metrics_param_dict[staff_id] = metrics_params_dict_entry
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_fname + rqst_lname)
    else:
        rqst_errors.append('Length of first name list must be equal to length of last name list')

    return metrics_dict


def retrieve_first_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_fname, list_of_first_names, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for first_name in list_of_first_names:
        first_name_ids = PICStaff.objects.filter(first_name__iexact=first_name).values_list('id', flat=True)
        if len(first_name_ids) > 0:
            list_of_ids.append(first_name_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Metrics for staff member with first name: {!s} not found in database'.format(first_name))
            response_raw_data["Status"]["Missing Parameters"].append(first_name)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                staff_id = metrics_submission.staff_member.id
                staff_info_dict = metrics_submission.staff_member.return_values_dict()

                metrics_params_dict_entry = {
                    "Metrics Data": [filtered_values_dict],
                    "Staff Information": staff_info_dict
                }
                if metrics_submission.staff_member.first_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.first_name] = {staff_id: metrics_params_dict_entry}
                else:
                    metrics_param_dict = metrics_dict[metrics_submission.staff_member.first_name]

                    if staff_id in metrics_param_dict:
                        metrics_param_dict[staff_id]["Metrics Data"].append(filtered_values_dict)
                    else:
                        metrics_param_dict[staff_id] = metrics_params_dict_entry
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_fname)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_fname)

    return metrics_dict


def retrieve_last_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_lname, list_of_last_names, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for last_name in list_of_last_names:
        last_name_ids = PICStaff.objects.filter(last_name__iexact=last_name).values_list('id', flat=True)
        if len(last_name_ids) > 0:
            list_of_ids.append(last_name_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Metrics for staff member with last name: {!s} not found in database'.format(last_name))
            response_raw_data["Status"]["Missing Parameters"].append(last_name)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                staff_id = metrics_submission.staff_member.id
                staff_info_dict = metrics_submission.staff_member.return_values_dict()

                metrics_params_dict_entry = {
                    "Metrics Data": [filtered_values_dict],
                    "Staff Information": staff_info_dict
                }

                if metrics_submission.staff_member.last_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.last_name] = {staff_id: metrics_params_dict_entry}
                else:
                    metrics_param_dict = metrics_dict[metrics_submission.staff_member.last_name]

                    if staff_id in metrics_param_dict:
                        metrics_param_dict[staff_id]["Metrics Data"].append(filtered_values_dict)
                    else:
                        metrics_param_dict[staff_id] = metrics_params_dict_entry
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_lname)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_lname)

    return metrics_dict


def retrieve_email_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_email, list_of_emails, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for email in list_of_emails:
        email_ids = PICStaff.objects.filter(email__iexact=email).values_list('id', flat=True)
        if len(email_ids) > 0:
            list_of_ids.append(email_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Staff member with email: {!s} not found in database'.format(email))
            response_raw_data["Status"]["Missing Parameters"].append(email)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                staff_id = metrics_submission.staff_member.id
                staff_info_dict = metrics_submission.staff_member.return_values_dict()

                metrics_params_dict_entry = {
                    "Metrics Data": [filtered_values_dict],
                    "Staff Information": staff_info_dict
                }

                if metrics_submission.staff_member.email not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.email] = {staff_id: metrics_params_dict_entry}
                else:
                    metrics_param_dict = metrics_dict[metrics_submission.staff_member.email]

                    if staff_id in metrics_param_dict:
                        metrics_param_dict[staff_id]["Metrics Data"].append(filtered_values_dict)
                    else:
                        metrics_param_dict[staff_id] = metrics_params_dict_entry
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_email)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_email)

    return metrics_dict


def retrieve_mpn_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_mpn, list_of_mpns, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for mpn in list_of_mpns:
        mpn_ids = PICStaff.objects.filter(mpn__iexact=mpn).values_list('id', flat=True)
        if len(mpn_ids) > 0:
            list_of_ids.append(mpn_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Staff member with mpn: {!s} not found in database'.format(mpn))
            response_raw_data["Status"]["Missing Parameters"].append(mpn)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                staff_id = metrics_submission.staff_member.id
                staff_info_dict = metrics_submission.staff_member.return_values_dict()

                metrics_params_dict_entry = {
                    "Metrics Data": [filtered_values_dict],
                    "Staff Information": staff_info_dict
                }

                staff_mpn = metrics_submission.staff_member.mpn
                if staff_mpn == '':
                    staff_mpn = "None"
                if staff_mpn not in metrics_dict:
                    metrics_dict[staff_mpn] = {staff_id: metrics_params_dict_entry}
                else:
                    metrics_param_dict = metrics_dict[staff_mpn]

                    if staff_id in metrics_param_dict:
                        metrics_param_dict[staff_id]["Metrics Data"].append(filtered_values_dict)
                    else:
                        metrics_param_dict[staff_id] = metrics_params_dict_entry
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for mpn(s): {!s} not found in database'.format(rqst_staff_mpn))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_mpn)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for mpn(s): {!s} not found in database'.format(rqst_staff_mpn))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_mpn)

    return metrics_dict


# def retrieve_location_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_location, fields=None):
#     metrics_submissions = metrics_submissions.filter(location__name__iexact=rqst_location)
#
#     metrics_dict = {}
#     if len(metrics_submissions) > 0:
#         for metrics_submission in metrics_submissions:
#             values_dict = metrics_submission.return_values_dict()
#             filtered_values_dict = {}
#             if fields:
#                 for field in fields:
#                     filtered_values_dict[field] = values_dict[field]
#             else:
#                 filtered_values_dict = values_dict
#
#             staff_id = metrics_submission.staff_member.id
#             staff_info_dict = metrics_submission.staff_member.return_values_dict()
#
#             metrics_params_dict_entry = {
#                 "Metrics Data": [filtered_values_dict],
#                 "Staff Information": staff_info_dict
#             }
#
#             location_name = metrics_submission.location.name
#             if location_name not in metrics_dict:
#                 metrics_dict[location_name] = {staff_id: metrics_params_dict_entry}
#             else:
#                 metrics_param_dict = metrics_dict[location_name]
#
#                 if staff_id in metrics_param_dict:
#                     metrics_param_dict[staff_id]["Metrics Data"].append(filtered_values_dict)
#                 else:
#                     metrics_param_dict[staff_id] = metrics_params_dict_entry
#     else:
#         if response_raw_data['Status']['Error Code'] != 2:
#             rqst_errors.append('No metrics entries for location(s): {!s} found in database'.format(rqst_location))
#
#     return metrics_dict
