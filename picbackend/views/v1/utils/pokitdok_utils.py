"""
Defines utility functions and classes for pokitdok views
- Need to obtain valid NPI
"""

from .base import clean_json_string_input
import pokitdok


def fetch_and_parse_pokit_elig_data(post_json, response_raw_data, post_errors):
    rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors, none_allowed=True)
    rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors, none_allowed=True)
    rqst_consumer_birth = clean_json_string_input(post_json, "root", "Birth Date", post_errors, none_allowed=True)
    rqst_consumer_plan_id = clean_json_string_input(post_json, "root", "Consumer Plan ID", post_errors,
                                                    none_allowed=True)
    rqst_consumer_gender = clean_json_string_input(post_json, "root", "Gender", post_errors,
                                                    none_allowed=True)
    rqst_consumer_trading_partner = clean_json_string_input(post_json, "root", "Trading Partner ID", post_errors)

    # if no errors, make request to pokitdok
    if len(post_errors) == 0:
        eligibility_data = {
            "member": {},
            "trading_partner_id": rqst_consumer_trading_partner
        }
        if rqst_consumer_f_name:
            eligibility_data["member"]["first_name"] = rqst_consumer_f_name
        if rqst_consumer_l_name:
            eligibility_data["member"]["last_name"] = rqst_consumer_l_name
        if rqst_consumer_birth:
            eligibility_data["member"]["birth_date"] = rqst_consumer_birth
        if rqst_consumer_plan_id:
            eligibility_data["member"]["id"] = rqst_consumer_plan_id
        if rqst_consumer_gender:
            eligibility_data["member"]["gender"] = rqst_consumer_gender

        pd = pokitdok.api.connect('fbSgQ0sM3xQNI5m8TyxR', 'du6JkRfNcHt8wNashtpf7Mdr96thZyn8Kilo9xoB')
        eligibility_results = pd.eligibility(eligibility_data)
        eligibility_results = check_elig_results_for_errors(eligibility_results, post_errors)

        parsed_elig_dict = {}
        if "No Data in response from Pokitdok" not in post_errors and "Errors in Pokitdok Data" not in post_errors:
            if rqst_consumer_trading_partner == "united_health_care":
                parse_united_health_care_data(eligibility_results, parsed_elig_dict, post_errors)
            elif rqst_consumer_trading_partner == "ambetter":
                parse_ambetter_data(eligibility_results, parsed_elig_dict, post_errors)
            else:
                parse_united_health_care_data(eligibility_results, parsed_elig_dict, post_errors)

        response_raw_data["Data"] = parsed_elig_dict
        # response_raw_data["Pokitdok Request"] = eligibility_data

    return response_raw_data


def parse_united_health_care_data(eligibility_results, parsed_elig_dict, post_errors):
    parse_elig_consumer_info(eligibility_results, parsed_elig_dict, post_errors)
    parse_elig_service_types(eligibility_results, parsed_elig_dict, post_errors)
    parse_elig_payer(eligibility_results, parsed_elig_dict, post_errors)

    coverage_dict = parse_elig_coverage_dict(eligibility_results, post_errors)
    if coverage_dict:
        parse_elig_deductibles_info(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_group_no(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_coinsurance(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_plan_start(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_out_of_pocket_info(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_copay(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_is_plan_active(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_insurace_type(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_plan_description(coverage_dict, parsed_elig_dict, post_errors)


def parse_ambetter_data(eligibility_results, parsed_elig_dict, post_errors):
    parse_elig_consumer_info(eligibility_results, parsed_elig_dict, post_errors)
    parse_elig_service_types(eligibility_results, parsed_elig_dict, post_errors)
    parse_elig_payer(eligibility_results, parsed_elig_dict, post_errors)

    coverage_dict = parse_elig_coverage_dict(eligibility_results, post_errors)
    if coverage_dict:
        parse_elig_deductibles_info(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_group_no(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_coinsurance(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_plan_start(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_out_of_pocket_info(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_is_plan_active(coverage_dict, parsed_elig_dict, post_errors)
        parse_elig_plan_description(coverage_dict, parsed_elig_dict, post_errors)


def parse_errors_key_in_elig_data(errors_obj, results):
    for key in errors_obj:
        if type(errors_obj[key]) is dict:
            parse_errors_key_in_elig_data(errors_obj[key], results)
        elif type(errors_obj[key]) is list:
            for error in errors_obj[key]:
                results.append(error)


def check_elig_results_for_errors(eligibility_results, post_errors):
    if "data" in eligibility_results:
        eligibility_results = eligibility_results["data"]

        if "valid_request" in eligibility_results:
            if eligibility_results["valid_request"] is False:
                post_errors.append("Pokitdok says Request is not valid")
        else:
            post_errors.append("Data has no valid_request parameter")
        if "reject_reason" in eligibility_results:
            post_errors.append(eligibility_results["reject_reason"])
        if "errors" in eligibility_results:
            data_errors = []
            parse_errors_key_in_elig_data(eligibility_results["errors"], data_errors)
            if data_errors:
                post_errors.append("Errors in Pokitdok Data")
                for error in data_errors:
                    post_errors.append(error)
    else:
        post_errors.append("No Data in response from Pokitdok")

    return eligibility_results


def parse_elig_payer(eligibility_results, parsed_elig_dict, post_errors):
    if "payer" in eligibility_results:
        parsed_elig_dict["Payer Info"] = eligibility_results["payer"]
    else:
        post_errors.append("Payer Info not found.")
        parsed_elig_dict["Payer Info"] = None


def parse_elig_consumer_info(eligibility_results, parsed_elig_dict, post_errors):
    if "subscriber" in eligibility_results:
        parsed_elig_dict["Consumer Info"] = eligibility_results["subscriber"]
    else:
        post_errors.append("Consumer Info not found.")
        parsed_elig_dict["Consumer Info"] = None


def parse_elig_service_types(eligibility_results, parsed_elig_dict, post_errors):
    if "service_types" in eligibility_results:
        parsed_elig_dict["Service Types"] = eligibility_results["service_types"]
    else:
        post_errors.append("Service Types not found.")
        parsed_elig_dict["Service Types"] = None


def parse_elig_coverage_dict(eligibility_results, post_errors):
    if "coverage" in eligibility_results:
        return eligibility_results["coverage"]
    else:
        post_errors.append("Coverage information not found in Pokitdok data.")
        return None


def parse_elig_group_no(coverage_dict, parsed_elig_dict, post_errors):
    if "group_number" in coverage_dict:
        parsed_elig_dict["Consumer Group Number"] = coverage_dict["group_number"]
    else:
        parsed_elig_dict["Consumer Group Number"] = None
        post_errors.append("Consumer group number not found in coverage dict.")


def parse_elig_coinsurance(coverage_dict, parsed_elig_dict, post_errors):
    if "coinsurance" in coverage_dict:
        parsed_elig_dict["Coinsurance Benefits"] = coverage_dict["coinsurance"]
    else:
        parsed_elig_dict["Coinsurance Benefits"] = None
        post_errors.append("Coinsurance Benefits not found in coverage dict.")


def parse_elig_plan_start(coverage_dict, parsed_elig_dict, post_errors):
    if "plan_begin_date" in coverage_dict:
        parsed_elig_dict["Plan Start Date"] = coverage_dict["plan_begin_date"]
    else:
        parsed_elig_dict["Plan Start Date"] = None
        post_errors.append("Plan Start Date not found in coverage dict.")


def parse_elig_copay(coverage_dict, parsed_elig_dict, post_errors):
    if "copay" in coverage_dict:
        parsed_elig_dict["Copay"] = coverage_dict["copay"]
    else:
        parsed_elig_dict["Copay"] = None
        post_errors.append("Copay not found in coverage dict.")


def parse_elig_is_plan_active(coverage_dict, parsed_elig_dict, post_errors):
    if "active" in coverage_dict:
        parsed_elig_dict["Plan is Active"] = coverage_dict["active"]
    else:
        parsed_elig_dict["Plan is Active"] = None
        post_errors.append("Plan is Active not found in coverage dict.")


def parse_elig_insurace_type(coverage_dict, parsed_elig_dict, post_errors):
    if "insurance_type" in coverage_dict:
        parsed_elig_dict["Insurance Type"] = coverage_dict["insurance_type"]
    else:
        parsed_elig_dict["Insurance Type"] = None
        post_errors.append("Insurance Type not found in coverage dict.")


def parse_elig_plan_description(coverage_dict, parsed_elig_dict, post_errors):
    if "plan_description" in coverage_dict:
        parsed_elig_dict["Plan Description"] = coverage_dict["plan_description"]
    else:
        parsed_elig_dict["Plan Description"] = None
        post_errors.append("Plan Description not found in coverage dict.")


def parse_elig_deductibles_info(coverage_dict, parsed_elig_dict, post_errors):
    if "deductibles" in coverage_dict:
        deductibles_data = coverage_dict["deductibles"]
        parsed_elig_dict["Deductibles"] = {}
        parsed_elig_dict["Deductibles"]["Calendar Year Amounts"] = parse_cal_year_amounts(deductibles_data)
    else:
        parsed_elig_dict["Deductibles"] = None
        post_errors.append("Deductibles info not found in coverage dict.")


def parse_elig_out_of_pocket_info(coverage_dict, parsed_elig_dict, post_errors):
    if "out_of_pocket" in coverage_dict:
        out_of_pocket_data = coverage_dict["out_of_pocket"]
        parsed_elig_dict["Out of Pocket"] = {}
        parsed_elig_dict["Out of Pocket"]["Calendar Year Amounts"] = parse_cal_year_amounts(out_of_pocket_data)
    else:
        parsed_elig_dict["Out of Pocket"] = None
        post_errors.append("Out of Pocket info not found in coverage dict.")


def parse_cal_year_amounts(poki_data):
    return_list = []

    for entry in poki_data:
        if ("time_period" in entry and entry["time_period"] == "calendar_year") or "time_period" not in entry:
            return_list.append(entry)

    return return_list

    # return_dict = {"In network": {"Family": None,
    #                               "Individual": None},
    #                "Out of network": {"Family": None,
    #                                   "Individual": None},
    #                "Network not applicable": {"Family": None,
    #                                           "Individual": None}}
    # for entry in poki_data:
    #     if "time_period" in entry and entry["time_period"] == "calendar_year":
    #         if "in_plan_network" in entry and entry["in_plan_network"] == "yes":
    #             if "coverage_level" in entry and entry["coverage_level"] == "family":
    #                 if "benefit_amount" in entry:
    #                     benefit_dict = entry["benefit_amount"]
    #                     if "amount" in benefit_dict and "currency" in benefit_dict:
    #                         return_dict["In network"]["Family"] = benefit_dict["amount"] + ' ' + benefit_dict["currency"]
    #             if "coverage_level" in entry and entry["coverage_level"] == "individual":
    #                 if "benefit_amount" in entry:
    #                     benefit_dict = entry["benefit_amount"]
    #                     if "amount" in benefit_dict and "currency" in benefit_dict:
    #                         return_dict["In network"]["Individual"] = benefit_dict["amount"] + ' ' + benefit_dict["currency"]
    #         if "in_plan_network" in entry and entry["in_plan_network"] == "no":
    #             if "coverage_level" in entry and entry["coverage_level"] == "family":
    #                 if "benefit_amount" in entry:
    #                     benefit_dict = entry["benefit_amount"]
    #                     if "amount" in benefit_dict and "currency" in benefit_dict:
    #                         return_dict["Out of network"]["Family"] = benefit_dict["amount"] + ' ' + benefit_dict["currency"]
    #             if "coverage_level" in entry and entry["coverage_level"] == "individual":
    #                 if "benefit_amount" in entry:
    #                     benefit_dict = entry["benefit_amount"]
    #                     if "amount" in benefit_dict and "currency" in benefit_dict:
    #                         return_dict["Out of network"]["Individual"] = benefit_dict["amount"] + ' ' + benefit_dict["currency"]
    #         if "in_plan_network" in entry and entry["in_plan_network"] == "not_applicable":
    #             if "coverage_level" in entry and entry["coverage_level"] == "family":
    #                 if "benefit_amount" in entry:
    #                     benefit_dict = entry["benefit_amount"]
    #                     if "amount" in benefit_dict and "currency" in benefit_dict:
    #                         return_dict["Network not applicable"]["Family"] = benefit_dict["amount"] + ' ' + benefit_dict["currency"]
    #             if "coverage_level" in entry and entry["coverage_level"] == "individual":
    #                 if "benefit_amount" in entry:
    #                     benefit_dict = entry["benefit_amount"]
    #                     if "amount" in benefit_dict and "currency" in benefit_dict:
    #                         return_dict["Network not applicable"]["Individual"] = benefit_dict["amount"] + ' ' + benefit_dict["currency"]

    # return return_dict
