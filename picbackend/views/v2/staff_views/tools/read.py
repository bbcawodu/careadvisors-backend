"""
Defines utility functions and classes for staff views
"""

from picmodels.models import PICStaff


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