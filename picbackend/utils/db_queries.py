from picmodels.models import PICStaff
import datetime, re, math


def build_search_params(rqst_params, response_raw_data, rqst_errors):
    search_params = {}
    if 'fname' in rqst_params:
        search_params['first name'] = rqst_params['fname']
        search_params['first name list'] = re.findall(r"[\w. '-]+", search_params['first name'])
    if 'lname' in rqst_params:
        search_params['last name'] = rqst_params['lname']
        search_params['last name list'] = re.findall(r"[\w. '-]+", search_params['last name'])
    if 'email' in rqst_params:
        search_params['email'] = rqst_params['email']
        search_params['email list'] = re.findall(r"[@\w. '-]+", search_params['email'])
    if 'id' in rqst_params:
        search_params['id'] = rqst_params['id']
        if search_params['id'] != "all":
            list_of_ids = re.findall("\d+", search_params['id'])
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            search_params['id list'] = list_of_ids
    if 'partnerid' in rqst_params:
        search_params['partnerid'] = rqst_params['partnerid']
        list_of_ids = re.findall("[@\w. '-_]+", search_params['partnerid'])
        search_params['partnerid list'] = list_of_ids
    if 'navid' in rqst_params:
        search_params['navigator id'] = rqst_params['navid']

        list_of_nav_ids = re.findall("\d+", search_params['navigator id'])
        for indx, element in enumerate(list_of_nav_ids):
            list_of_nav_ids[indx] = int(element)
        search_params['navigator id list'] = list_of_nav_ids
    if 'page' in rqst_params:
        search_params['page number'] = int(rqst_params['page'])
    if "county" in rqst_params:
        search_params['county'] = rqst_params['county']
        search_params['county list'] = re.findall(r"[\w. '-]+", search_params['county'])
    if "zipcode" in rqst_params:
        search_params['zipcode'] = rqst_params['zipcode']
        search_params['zipcode list'] = re.findall(r"\d+", search_params['zipcode'])
    if "time" in rqst_params:
        try:
            search_params['look up date'] = datetime.date.today() - datetime.timedelta(days=rqst_params['time'])
            search_params['time'] = rqst_params['time']
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('time parameter must be a valid integer. Metrics returned without time parameter.')
    if "startdate" in rqst_params:
        try:
            datetime.datetime.strptime(rqst_params["startdate"], '%Y-%m-%d')
            search_params['start date'] = rqst_params["startdate"]
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('startdate parameter must be a valid date. Metrics returned without startdate parameter.')
    if "enddate" in rqst_params:
        try:
            datetime.datetime.strptime(rqst_params["enddate"], '%Y-%m-%d')
            search_params['end date'] = rqst_params["enddate"]
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('enddate parameter must be a valid integer. Metrics returned without enddate parameter.')
    if "groupby" in rqst_params:
        search_params['group by'] = rqst_params['groupby']

    return search_params


def retrieve_f_l_name_staff(response_raw_data, rqst_errors, staff_members, rqst_first_name, rqst_last_name):
    staff_members = staff_members.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)
    if len(staff_members) > 0:
        staff_member_dict = {}
        rqst_full_name = rqst_first_name + " " + rqst_last_name
        for staff_member in staff_members:
            if rqst_full_name not in staff_member_dict:
                staff_member_dict[rqst_full_name] = [staff_member.return_values_dict()]
            else:
                staff_member_dict[rqst_full_name].append(staff_member.return_values_dict())

        staff_member_list = []
        for staff_key, staff_entry in staff_member_dict.items():
            staff_member_list.append(staff_entry)
        response_raw_data["Data"] = staff_member_list
    else:
        rqst_errors.append('Staff Member with name: {!s} {!s} not found in database'.format(rqst_first_name,
                                                                                            rqst_last_name))

    return response_raw_data, rqst_errors


def retrieve_email_staff(response_raw_data, rqst_errors, rqst_email, list_of_emails):
    staff_dict = {}
    for email in list_of_emails:
        staff_members = PICStaff.objects.filter(email__iexact=email)
        for staff_member in staff_members:
            if email not in staff_dict:
                staff_dict[email] = [staff_member.return_values_dict()]
            else:
                staff_dict[email].append(staff_member.return_values_dict())
    if len(staff_dict) > 0:
        staff_list = []
        for staff_key, staff_entry in staff_dict.items():
            staff_list.append(staff_entry)
        response_raw_data["Data"] = staff_list
        for email in list_of_emails:
            if email not in staff_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member with email: {!s} not found in database'.format(email))
    else:
        rqst_errors.append('Staff Member with emails(s): {!s} not found in database'.format(rqst_email))

    return response_raw_data, rqst_errors


def retrieve_first_name_staff(response_raw_data, rqst_errors, rqst_first_name, list_of_first_names):
    staff_dict = {}
    for first_name in list_of_first_names:
        staff_members = PICStaff.objects.filter(first_name__iexact=first_name)
        for staff_member in staff_members:
            if first_name not in staff_dict:
                staff_dict[first_name] = [staff_member.return_values_dict()]
            else:
                staff_dict[first_name].append(staff_member.return_values_dict())
    if len(staff_dict) > 0:
        staff_list = []
        for staff_key, staff_entry in staff_dict.items():
            staff_list.append(staff_entry)
        response_raw_data["Data"] = staff_list
        for name in list_of_first_names:
            if name not in staff_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member with first name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Staff Member with first name(s): {!s} not found in database'.format(rqst_first_name))

    return response_raw_data, rqst_errors


def retrieve_last_name_staff(response_raw_data, rqst_errors, rqst_last_name, list_of_last_names):
    staff_dict = {}
    for last_name in list_of_last_names:
        staff_members = PICStaff.objects.filter(last_name__iexact=last_name)
        for staff_member in staff_members:
            if last_name not in staff_dict:
                staff_dict[last_name] = [staff_member.return_values_dict()]
            else:
                staff_dict[last_name].append(staff_member.return_values_dict())
    if len(staff_dict) > 0:
        staff_list = []
        for staff_key, staff_entry in staff_dict.items():
            staff_list.append(staff_entry)
        response_raw_data["Data"] = staff_list
        for name in list_of_last_names:
            if name not in staff_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member with last name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Staff Member with last name(s): {!s} not found in database'.format(rqst_last_name))

    return response_raw_data, rqst_errors


def retrieve_county_staff(response_raw_data, rqst_errors, rqst_county, list_of_counties):
    staff_dict = {}
    for county in list_of_counties:
        staff_members = PICStaff.objects.filter(county__iexact=county)
        for staff_member in staff_members:
            if county not in staff_dict:
                staff_dict[county] = [staff_member.return_values_dict()]
            else:
                staff_dict[county].append(staff_member.return_values_dict())
    if len(staff_dict) > 0:
        staff_list = []
        for staff_key, staff_entry in staff_dict.items():
            staff_list.append(staff_entry)
        response_raw_data["Data"] = staff_list
        for county in list_of_counties:
            if county not in staff_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member(s) with county: {!s} not found in database'.format(county))
    else:
        rqst_errors.append('Staff Member(s) with county(s): {!s} not found in database'.format(rqst_county))

    return response_raw_data, rqst_errors


def retrieve_id_staff(response_raw_data, rqst_errors, rqst_staff_id, list_of_ids):
    if rqst_staff_id == "all":
        all_staff_members = PICStaff.objects.all()
        staff_member_dict = {}
        for staff_member in all_staff_members:
            staff_member_dict[staff_member.id] = staff_member.return_values_dict()
        staff_list = []
        for staff_key, staff_entry in staff_member_dict.items():
            staff_list.append(staff_entry)
        response_raw_data["Data"] = staff_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            staff_members = PICStaff.objects.filter(id__in=list_of_ids)
            if len(staff_members) > 0:
                staff_dict = {}
                for staff_member in staff_members:
                    staff_dict[staff_member.id] = staff_member.return_values_dict()
                staff_list = []
                for staff_key, staff_entry in staff_dict.items():
                    staff_list.append(staff_entry)
                response_raw_data["Data"] = staff_list
                # response_raw_data["Data"] = staff_dict

                for staff_id in list_of_ids:
                    if staff_id not in staff_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Staff Member with id: {!s} not found in database'.format(str(staff_id)))
            else:
                rqst_errors.append('No staff members found for database ID(s): ' + rqst_staff_id)
        else:
            rqst_errors.append('No valid staff IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_f_l_name_consumers(response_raw_data, rqst_errors, consumers, rqst_first_name, rqst_last_name):
    consumers = consumers.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)
    if len(consumers) > 0:
        consumer_dict = {}
        rqst_full_name = rqst_first_name + " " + rqst_last_name
        for consumer in consumers:
            if rqst_full_name not in consumer_dict:
                consumer_dict[rqst_full_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[rqst_full_name].append(consumer.return_values_dict())

        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
    else:
        rqst_errors.append('Consumer with name: {!s} {!s} not found in database'.format(rqst_first_name,
                                                                                            rqst_last_name))

    return response_raw_data, rqst_errors


def retrieve_email_consumers(response_raw_data, rqst_errors, consumers, rqst_email, list_of_emails):
    consumer_dict = {}
    consumers_object = consumers
    for email in list_of_emails:
        consumers = consumers_object.filter(email__iexact=email)
        for consumer in consumers:
            if email not in consumer_dict:
                consumer_dict[email] = [consumer.return_values_dict()]
            else:
                consumer_dict[email].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for email in list_of_emails:
            if email not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Consumer with email: {!s} not found in database'.format(email))
    else:
        rqst_errors.append('Consumer with emails(s): {!s} not found in database'.format(rqst_email))

    return response_raw_data, rqst_errors


def retrieve_first_name_consumers(response_raw_data, rqst_errors, consumers, rqst_first_name, list_of_first_names):
    consumer_dict = {}
    consumers_object = consumers
    for first_name in list_of_first_names:
        consumers = consumers_object.filter(first_name__iexact=first_name)
        for consumer in consumers:
            if first_name not in consumer_dict:
                consumer_dict[first_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[first_name].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for name in list_of_first_names:
            if name not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Consumer with first name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Consumer with first name(s): {!s} not found in database'.format(rqst_first_name))

    return response_raw_data, rqst_errors


def retrieve_last_name_consumers(response_raw_data, rqst_errors, consumers, rqst_last_name, list_of_last_names):
    consumer_dict = {}
    consumers_object = consumers
    for last_name in list_of_last_names:
        consumers = consumers_object.filter(last_name__iexact=last_name)
        for consumer in consumers:
            if last_name not in consumer_dict:
                consumer_dict[last_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[last_name].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for name in list_of_last_names:
            if name not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member with last name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Staff Member with last name(s): {!s} not found in database'.format(rqst_last_name))

    return response_raw_data, rqst_errors


def retrieve_id_consumers(response_raw_data, rqst_errors, consumers, rqst_consumer_id, list_of_ids):
    if rqst_consumer_id == "all":
        all_consumers = consumers
        consumer_dict = {}
        for consumer in all_consumers:
            consumer_dict[consumer.id] = consumer.return_values_dict()
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)

        response_raw_data["Data"] = consumer_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            consumers = consumers.filter(id__in=list_of_ids)
            if len(consumers) > 0:

                consumer_dict = {}
                for consumer in consumers:
                    consumer_dict[consumer.id] = consumer.return_values_dict()
                consumer_list = []
                for consumer_key, consumer_entry in consumer_dict.items():
                    consumer_list.append(consumer_entry)
                response_raw_data["Data"] = consumer_list

                for consumer_id in list_of_ids:
                    if consumer_id not in consumer_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Consumer with id: {!s} not found in database'.format(str(consumer_id)))
            else:
                rqst_errors.append('No consumers found for database ID(s): ' + rqst_consumer_id)
        else:
            rqst_errors.append('No valid consumer IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def break_results_into_pages(request, response_raw_data, CONSUMERS_PER_PAGE, rqst_page_no):
    consumer_list = response_raw_data["Data"]
    if len(consumer_list) > CONSUMERS_PER_PAGE:
        if rqst_page_no:
            if len(consumer_list) > ((rqst_page_no - 1) * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[:(CONSUMERS_PER_PAGE * (rqst_page_no - 1))]):
                    consumer_list[i] = consumer["Database ID"]
            if len(consumer_list) > (rqst_page_no * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE):]):
                    consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE)+i] = consumer["Database ID"]
        else:
            response_raw_data["Page URLs"] = []
            total_pages = math.ceil(len(consumer_list) / CONSUMERS_PER_PAGE)
            for i in range(total_pages):
                response_raw_data["Page URLs"].append(request.build_absolute_uri(None) + "&page=" + str(i+1))

            for i, consumer in enumerate(consumer_list[CONSUMERS_PER_PAGE:]):
                consumer_list[CONSUMERS_PER_PAGE+i] = consumer["Database ID"]

    response_raw_data["Data"] = consumer_list
    return response_raw_data


# defines function to group metrics by given parameter
def group_metrics(metrics_dict, grouping_parameter):
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
                if metrics_entry[grouping_parameter] not in return_dict:
                    return_dict[metrics_entry[grouping_parameter]] = {staff_key: {"Metrics Data": [metrics_entry],
                                                                      "Staff Information": staff_dict["Staff Information"]}}
                else:
                    if staff_key not in return_dict[metrics_entry[grouping_parameter]]:
                        return_dict[metrics_entry[grouping_parameter]][staff_key] = {"Metrics Data": [metrics_entry],
                                                                                     "Staff Information": staff_dict["Staff Information"]}
                    else:
                        return_dict[metrics_entry[grouping_parameter]][staff_key]["Metrics Data"].append(metrics_entry)
    return return_dict


def retrieve_id_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_id, list_of_ids):
    if rqst_staff_id.lower() != "all":
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

    metrics_dict = {}
    if len(metrics_submissions) > 0:
        for metrics_submission in metrics_submissions:
            if metrics_submission.staff_member_id not in metrics_dict:
                metrics_dict[metrics_submission.staff_member_id] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                metrics_dict[metrics_submission.staff_member_id]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
            else:
                metrics_dict[metrics_submission.staff_member_id]["Metrics Data"].append(metrics_submission.return_values_dict())

        if rqst_staff_id.lower() != "all":
            for staff_id in list_of_ids:
                if staff_id not in metrics_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Metrics for staff Member with id: {!s} not found in database'.format(str(staff_id)))
    else:
        rqst_errors.append('No metrics entries for staff ID(s): {!s} not found in database'.format(rqst_staff_id))

    return metrics_dict


def retrieve_f_l_name_metrics(response_raw_data, rqst_errors, metrics_submissions, list_of_first_names, list_of_last_names, rqst_fname, rqst_lname):
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
        list_of_ids = list(set().union(*list_of_ids))
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                name = '{!s} {!s}'.format(metrics_submission.staff_member.first_name, metrics_submission.staff_member.last_name)
                if name not in metrics_dict:
                    metrics_dict[name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                    metrics_dict[name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[name]["Metrics Data"].append(metrics_submission.return_values_dict())
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))
    else:
        rqst_errors.append('Length of first name list must be equal to length of last name list')

    return metrics_dict


def retrieve_first_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_fname, list_of_first_names):
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
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                if metrics_submission.staff_member.first_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.first_name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                    metrics_dict[metrics_submission.staff_member.first_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.first_name]["Metrics Data"].append(metrics_submission.return_values_dict())
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))

    return metrics_dict


def retrieve_last_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_lname, list_of_last_names):
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
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                if metrics_submission.staff_member.last_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.last_name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                    metrics_dict[metrics_submission.staff_member.last_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.last_name]["Metrics Data"].append(metrics_submission.return_values_dict())
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))

    return metrics_dict


def retrieve_email_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_email, list_of_emails):
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
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                if metrics_submission.staff_member.email not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                    metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(metrics_submission.return_values_dict())
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))

    return metrics_dict
