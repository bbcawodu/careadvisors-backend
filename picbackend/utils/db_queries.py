from picmodels.models import PICStaff, CredentialsModel
import datetime, re, math, urllib, httplib2
from random import shuffle
from googleapiclient.discovery import build
from pandas.tseries.offsets import BDay
from pandas import bdate_range
from bdateutil import isbday
import dateutil.parser
from dateutil.tz import tzutc
import pytz
from googleapiclient.http import BatchHttpRequest


START_OF_BUSINESS_TIMESTAMP = datetime.time(hour=15, minute=0, second=0, microsecond=0)
END_OF_BUSINESS_TIMESTAMP = datetime.time(hour=23, minute=0, second=0, microsecond=0)

def build_search_params(rqst_params, response_raw_data, rqst_errors):
    search_params = {}
    if 'location' in rqst_params:
        search_params['location'] = urllib.parse.unquote(rqst_params['location'])
    if 'fields' in rqst_params:
        search_params['fields'] = urllib.parse.unquote(rqst_params['fields'])
        search_params['fields list'] = re.findall(r"[@\w. '-]+", search_params['fields'])
    if 'fname' in rqst_params:
        search_params['first name'] = rqst_params['fname']
        search_params['first name list'] = re.findall(r"[\w. '-]+", search_params['first name'])
    if 'lname' in rqst_params:
        search_params['last name'] = rqst_params['lname']
        search_params['last name list'] = re.findall(r"[\w. '-]+", search_params['last name'])
    if 'email' in rqst_params:
        search_params['email'] = rqst_params['email']
        search_params['email list'] = re.findall(r"[@\w. '-]+", search_params['email'])
    if 'mpn' in rqst_params:
        search_params['mpn'] = rqst_params['mpn']
        search_params['mpn list'] = re.findall(r"[@\w. '-]+", search_params['mpn'])
    if 'region' in rqst_params:
        search_params['region'] = rqst_params['region']
        search_params['region list'] = re.findall(r"[@\w. '-]+", search_params['region'])
    if 'id' in rqst_params:
        search_params['id'] = rqst_params['id']
        if search_params['id'] != "all":
            list_of_ids = re.findall("\d+", search_params['id'])
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            search_params['id list'] = list_of_ids

            if not search_params['id list']:
                rqst_errors.append('Invalid id, ids must be base 10 integers')
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

        if not search_params['navigator id list']:
            rqst_errors.append('Invalid navigator id, navigator ids must be base 10 integers')
    if 'page' in rqst_params:
        search_params['page number'] = int(rqst_params['page'])
    if "county" in rqst_params:
        search_params['county'] = rqst_params['county']
        search_params['county list'] = re.findall(r"[\w. '-]+", search_params['county'])
    if "zipcode" in rqst_params:
        search_params['zipcode'] = rqst_params['zipcode']
        search_params['zipcode list'] = re.findall(r"\d+", search_params['zipcode'])

        if not search_params['zipcode list']:
            rqst_errors.append('Invalid zipcode, zipcodes must be integers')
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
        rqst_errors.append('Staff Member with email(s): {!s} not found in database'.format(rqst_email))

    return response_raw_data, rqst_errors


def retrieve_mpn_staff(response_raw_data, rqst_errors, rqst_mpn, list_of_mpns):
    staff_dict = {}
    for mpn in list_of_mpns:
        staff_members = PICStaff.objects.filter(mpn__iexact=mpn)
        for staff_member in staff_members:
            if mpn not in staff_dict:
                staff_dict[mpn] = [staff_member.return_values_dict()]
            else:
                staff_dict[mpn].append(staff_member.return_values_dict())
    if len(staff_dict) > 0:
        staff_list = []
        for staff_key, staff_entry in staff_dict.items():
            staff_list.append(staff_entry)
        response_raw_data["Data"] = staff_list
        for mpn in list_of_mpns:
            if mpn not in staff_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member with mpn: {!s} not found in database'.format(mpn))
    else:
        rqst_errors.append('Staff Member with mpn(s): {!s} not found in database'.format(rqst_mpn))

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


def retrieve_region_staff(response_raw_data, rqst_errors, rqst_region, list_of_regions):
    staff_dict = {}

    region_mappings = PICStaff.REGIONS
    for region in list_of_regions:
        region_counties = region_mappings[region]
        for county in region_counties:
            staff_members = PICStaff.objects.filter(county__iexact=county)
            for staff_member in staff_members:
                if region not in staff_dict:
                    staff_dict[region] = [staff_member.return_values_dict()]
                else:
                    staff_dict[region].append(staff_member.return_values_dict())

    # staff_members = PICStaff.objects.filter(region__in=list_of_regions)
    # if len(staff_members) > 0:
    #     staff_dict = {}
    #     for staff_member in staff_members:
    #         staff_dict[staff_member.region] = staff_member.return_values_dict()

    if len(staff_dict) > 0:
        staff_list = []
        for staff_key, staff_entry in staff_dict.items():
            staff_list.append(staff_entry)
        response_raw_data["Data"] = staff_list
        for region in list_of_regions:
            if region not in staff_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member(s) with region: {!s} not found in database'.format(region))
    else:
        rqst_errors.append('Staff Member(s) with region(s): {!s} not found in database'.format(rqst_region))

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

                name = '{!s} {!s}'.format(metrics_submission.staff_member.first_name, metrics_submission.staff_member.last_name)
                if name not in metrics_dict:
                    metrics_dict[name] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[name]["Metrics Data"].append(filtered_values_dict)
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

                if metrics_submission.staff_member.first_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.first_name] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.first_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.first_name]["Metrics Data"].append(filtered_values_dict)
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

                if metrics_submission.staff_member.last_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.last_name] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.last_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.last_name]["Metrics Data"].append(filtered_values_dict)
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

                if metrics_submission.staff_member.email not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(filtered_values_dict)
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

                if metrics_submission.staff_member.email not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(filtered_values_dict)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for mpn(s): {!s} not found in database'.format(rqst_staff_mpn))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_mpn)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for mpn(s): {!s} not found in database'.format(rqst_staff_mpn))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_mpn)

    return metrics_dict


def retrieve_location_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_location, fields=None):
    metrics_submissions = metrics_submissions.filter(location__name__iexact=rqst_location)

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

            if metrics_submission.staff_member.email not in metrics_dict:
                metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [filtered_values_dict]}
                metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
            else:
                metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(filtered_values_dict)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for location(s): {!s} found in database'.format(rqst_location))

    return metrics_dict


def get_preferred_nav_apts(rqst_preferred_times, valid_rqst_preferred_times_timestamps, post_errors):
    preferred_appointments = []
    oldest_preferred_time_timestamp = min(valid_rqst_preferred_times_timestamps)
    max_preferred_time_timestamp = max(valid_rqst_preferred_times_timestamps) + datetime.timedelta(hours=1)

    nav_free_busy_list = get_nav_free_busy_times(oldest_preferred_time_timestamp, max_preferred_time_timestamp)

    for preferred_time_iso_string in rqst_preferred_times:
        shuffle(nav_free_busy_list)
        preferred_appointments_list = []

        if not isinstance(preferred_time_iso_string, str):
            post_errors.append("{!s} is not a string, Preferred Times must be a string iso formatted date and time".format(str(preferred_time_iso_string)))
        else:
            try:
                preferred_time_timestamp = dateutil.parser.parse(preferred_time_iso_string).replace(tzinfo=pytz.UTC)

                for nav_free_busy_entry in nav_free_busy_list:
                    nav_info = nav_free_busy_entry[0]
                    nav_busy_list = nav_free_busy_entry[1]
                    if not nav_busy_list:
                        preferred_appointments_list.append(create_navigator_apt_entry(nav_info, preferred_time_timestamp))
                        break
                    else:
                        nav_is_busy = False
                        for busy_time_dict in nav_busy_list:
                            start_date_time = dateutil.parser.parse(busy_time_dict['start'])
                            end_date_time = dateutil.parser.parse(busy_time_dict['end'])
                            if start_date_time <= preferred_time_timestamp < end_date_time:
                                nav_is_busy = True
                                break

                        if not nav_is_busy:
                            preferred_appointments_list.append(create_navigator_apt_entry(nav_info, preferred_time_timestamp))
                            break

            except ValueError:
                post_errors.append("{!s} is not a properly iso formatted date and time, Preferred Times must be a string iso formatted date and time".format(preferred_time_iso_string))

        preferred_appointments.append(preferred_appointments_list)

    return preferred_appointments


def get_next_available_nav_apts(post_errors):
    next_available_appointments = []

    now_date_time = datetime.datetime.utcnow()
    earliest_available_date_time = get_earliest_available_apt_datetime(now_date_time)

    end_of_next_b_day_date_time = earliest_available_date_time + BDay(1)
    end_of_next_b_day_date_time = end_of_next_b_day_date_time.replace(hour=23, minute=0, second=0, microsecond=0)

    credentials_objects = CredentialsModel.objects.all()
    if credentials_objects:
        while not next_available_appointments:
            possible_appointment_times = get_possible_appointments_range(earliest_available_date_time, end_of_next_b_day_date_time)
            nav_free_busy_list = get_nav_free_busy_times(earliest_available_date_time, end_of_next_b_day_date_time)

            for appointment_time in possible_appointment_times:
                shuffle(nav_free_busy_list)

                for nav_free_busy_entry in nav_free_busy_list:
                    nav_info = nav_free_busy_entry[0]
                    nav_busy_list = nav_free_busy_entry[1]
                    if not nav_busy_list:
                        next_available_appointments.append(create_navigator_apt_entry(nav_info, appointment_time))
                        break
                    else:
                        nav_is_busy = False
                        for busy_time_dict in nav_busy_list:
                            start_date_time = dateutil.parser.parse(busy_time_dict['start'])
                            end_date_time = dateutil.parser.parse(busy_time_dict['end'])
                            if start_date_time <= appointment_time < end_date_time:
                                nav_is_busy = True
                                break

                        if not nav_is_busy:
                            next_available_appointments.append(create_navigator_apt_entry(nav_info, appointment_time))
                            break

            if not next_available_appointments:
                earliest_available_date_time = end_of_next_b_day_date_time + BDay(1)
                earliest_available_date_time = earliest_available_date_time.replace(hour=15, minute=0, second=0, microsecond=0)

                end_of_next_b_day_date_time = earliest_available_date_time + BDay(1)
                end_of_next_b_day_date_time = end_of_next_b_day_date_time.replace(hour=23, minute=0, second=0, microsecond=0)
    else:
        post_errors.append("No Navigators with Authorized credentials to query from. Next Available Appointments will be empty.")

    return next_available_appointments


def get_nav_free_busy_times(start_timestamp, end_timestamp):
    nav_cal_list_dict = get_nav_cal_lists()

    nav_free_busy_list = get_free_busy_list(start_timestamp, end_timestamp, nav_cal_list_dict)

    return nav_free_busy_list


def create_navigator_apt_entry(nav_info, appointment_timestamp):
    next_available_apt_entry = {"Navigator Name": "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"]),
                                "Navigator Database ID": nav_info["Database ID"],
                                "Appointment Date and Time": appointment_timestamp.isoformat()[:-6],
                                "Schedule Appointment Link": "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid={!s}".format(str(nav_info["Database ID"])),
                                }

    return next_available_apt_entry


def get_earliest_available_apt_datetime(now_date_time):
    if not isbday(now_date_time):
        earliest_available_date_time = now_date_time + BDay(1)
        earliest_available_date_time = earliest_available_date_time.replace(hour=15, minute=0, second=0, microsecond=0)
    else:
        current_time = datetime.time(hour=now_date_time.hour, minute=now_date_time.minute, second=now_date_time.second, microsecond=now_date_time.microsecond)

        if current_time > END_OF_BUSINESS_TIMESTAMP:
            earliest_available_date_time = now_date_time + BDay(1)
            earliest_available_date_time = earliest_available_date_time.replace(hour=15, minute=0, second=0, microsecond=0)
        elif current_time < START_OF_BUSINESS_TIMESTAMP:
            earliest_available_date_time = now_date_time.replace(hour=15, minute=0, second=0, microsecond=0)
        else:
            earliest_available_date_time = now_date_time

    return earliest_available_date_time


def get_possible_appointments_range(earliest_available_date_time, end_of_next_b_day_date_time):
    earliest_available_time = datetime.time(hour=earliest_available_date_time.hour, minute=earliest_available_date_time.minute, second=earliest_available_date_time.second, microsecond=earliest_available_date_time.microsecond)
    possible_appointment_times = []

    day_1_appointment_timesstamps = bdate_range(start=earliest_available_date_time, end=earliest_available_date_time + datetime.timedelta(days=1), freq='30min', tz=tzutc())
    day_1_appointment_timesstamps = day_1_appointment_timesstamps.tolist()

    for timestamp in day_1_appointment_timesstamps:
        timestamp_time = datetime.time(hour=timestamp.hour, minute=timestamp.minute, second=timestamp.second, microsecond=timestamp.microsecond)
        if earliest_available_time < timestamp_time < END_OF_BUSINESS_TIMESTAMP:
            possible_appointment_times.append(timestamp)

    day_2_appointment_timesstamps = bdate_range(start=end_of_next_b_day_date_time, end=end_of_next_b_day_date_time + datetime.timedelta(days=1), freq='30min', tz=tzutc())
    day_2_appointment_timesstamps = day_2_appointment_timesstamps.tolist()

    for timestamp in day_2_appointment_timesstamps:
        timestamp_time = datetime.time(hour=timestamp.hour, minute=timestamp.minute, second=timestamp.second, microsecond=timestamp.microsecond)
        if START_OF_BUSINESS_TIMESTAMP <= timestamp_time < END_OF_BUSINESS_TIMESTAMP:
            possible_appointment_times.append(timestamp)

    return possible_appointment_times


def get_nav_cal_lists():
    nav_cal_list_dict = {}

    def add_cal_list_entry(request_id, response, exception):
        nav_cal_list_dict[request_id] = response["items"]

    #build batch request
    cal_list_batch = BatchHttpRequest()

    credentials_objects = list(CredentialsModel.objects.all())
    while credentials_objects:
        credentials_object = credentials_objects.pop()
        nav_object = credentials_object.id

        if credentials_object.credential.invalid:
            credentials_object.delete()
        else:
            nav_cal_list_dict[str(nav_object.id)] = []

            #Obtain valid credential and use it to build authorized service object for given navigator
            credential = credentials_object.credential
            http = httplib2.Http()
            http = credential.authorize(http)
            service = build("calendar", "v3", http=http)

            cal_list_batch.add(service.calendarList().list(showHidden=True), callback=add_cal_list_entry, request_id=str(nav_object.id))
    cal_list_batch.execute()

    return nav_cal_list_dict


def get_free_busy_list(start_timestamp, end_timestamp, nav_cal_list_dict):
    nav_free_busy_dict = {}
    nav_free_busy_list = []

    def add_free_busy_entry(request_id, response, exception):
        for cals_key, calendar_object in response["calendars"].items():
            busy_list = calendar_object["busy"]
            if busy_list:
                for busy_entry in busy_list:
                    nav_free_busy_dict[request_id].append(busy_entry)

    #build batch request
    # Each HTTP connection that your application makes results in a certain amount of overhead. This library supports batching, to allow your application to put several API calls into a single HTTP request. Examples of situations when you might want to use batching:

    # You have many small requests to make and would like to minimize HTTP request overhead.
    # A user made changes to data while your application was offline, so your application needs to synchronize its local data with the server by sending a lot of updates and deletes.
    # Note: You're limited to 1000 calls in a single batch request. If you need to make more calls than that, use multiple batch requests
    free_busy_batch = BatchHttpRequest()

    credentials_objects = list(CredentialsModel.objects.all())
    while credentials_objects:
        credentials_object = credentials_objects.pop()
        nav_object = credentials_object.id

        if credentials_object.credential.invalid:
            credentials_object.delete()
        else:
            nav_free_busy_dict[str(nav_object.id)] = []

            #Obtain valid credential and use it to build authorized service object for given navigator
            credential = credentials_object.credential
            http = httplib2.Http()
            http = credential.authorize(http)
            service = build("calendar", "v3", http=http)

            nav_cal_list_object = nav_cal_list_dict[str(nav_object.id)]
            items_list = []
            for nav_cal_object in nav_cal_list_object:
                items_entry = {"id": nav_cal_object["id"]}
                items_list.append(items_entry)

            free_busy_args = {"timeMin": start_timestamp.isoformat() + 'Z', # 'Z' indicates UTC time
                              "timeMax": end_timestamp.isoformat() + 'Z',
                              "items": items_list}
            free_busy_batch.add(service.freebusy().query(body=free_busy_args), callback=add_free_busy_entry, request_id=str(nav_object.id))
    free_busy_batch.execute()

    for key, value in nav_free_busy_dict.items():
        nav_free_busy_list.append([PICStaff.objects.get(id=int(key)).return_values_dict(), value])

    return nav_free_busy_list


def get_nav_scheduled_appointments(nav_info, credentials_object, rqst_errors):
    scheduled_appointment_list = []
    credential = credentials_object.credential

    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("calendar", "v3", http=http)

    nav_cal_list = service.calendarList().list(showHidden=True).execute()["items"]
    nav_cal_id = None
    for calendar in nav_cal_list:
        calendar_name = calendar["summary"]
        if calendar_name == "Navigator-Consumer Appointments (DO NOT CHANGE)":
            nav_cal_id = calendar["id"]
    if not nav_cal_id:
        rqst_errors.append("Navigator-Consumer Appointments not found in Navigator's Google CalendarList")

    if not rqst_errors:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("calendar", "v3", http=http)

        nav_cal_events = service.events().list(calendarId=nav_cal_id,
                                               orderBy="startTime",
                                               showHiddenInvitations=True,
                                               singleEvents=True,
                                               timeMin=datetime.datetime.utcnow().isoformat() + 'Z').execute()["items"]

        if nav_cal_events:
            for cal_event in nav_cal_events:
                scheduled_appointment_entry = {"Navigator Name": "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"]),
                                               "Navigator Database ID": nav_info["Database ID"],
                                               "Appointment Date and Time": cal_event["start"]["dateTime"],
                                               "Appointment Summary": None}
                if "description" in cal_event:
                    scheduled_appointment_entry["Appointment Summary"] = cal_event["description"]
                scheduled_appointment_list.append(scheduled_appointment_entry)
        else:
            rqst_errors.append("No scheduled appointments in navigator's 'Navigator-Consumer Appointments' calendar")

    return scheduled_appointment_list
