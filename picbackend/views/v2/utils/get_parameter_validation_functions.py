import datetime
import re
import urllib


def validate_get_rqst_parameter_id(get_rqst_params, validated_params, rqst_errors):
    if 'id' in get_rqst_params:
        validated_params['id'] = get_rqst_params['id']
        if validated_params['id'] != "all":
            list_of_ids = re.findall("\d+", validated_params['id'])
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            validated_params['id list'] = list_of_ids

            if not validated_params['id list']:
                rqst_errors.append('Invalid id, ids must be base 10 integers')


def validate_get_rqst_parameter_fname(get_rqst_params, validated_params, rqst_errors):
    if 'fname' in get_rqst_params:
        validated_params['first name'] = get_rqst_params['fname']
        validated_params['first name list'] = re.findall(r"[\w. '-]+", validated_params['first name'])

        if not validated_params['first name list']:
            rqst_errors.append('Invalid first name, first names must be ascii strings.')


def validate_get_rqst_parameter_lname(get_rqst_params, validated_params, rqst_errors):
    if 'lname' in get_rqst_params:
        validated_params['last name'] = get_rqst_params['lname']
        validated_params['last name list'] = re.findall(r"[\w. '-]+", validated_params['last name'])

        if not validated_params['last name list']:
            rqst_errors.append('Invalid last name, last names must be ascii strings.')


def validate_get_rqst_parameter_email(get_rqst_params, validated_params, rqst_errors):
    if 'email' in get_rqst_params:
        validated_params['email'] = get_rqst_params['email']
        validated_params['email list'] = re.findall(r"[@\w. '-]+", validated_params['email'])

        if not validated_params['email list']:
            rqst_errors.append('Invalid email parameter.')


def validate_get_rqst_parameter_mpn(get_rqst_params, validated_params, rqst_errors):
    if 'mpn' in get_rqst_params:
        validated_params['mpn'] = get_rqst_params['mpn']
        validated_params['mpn list'] = re.findall(r"[@\w. '-]+", validated_params['mpn'])

        if not validated_params['mpn list']:
            rqst_errors.append('Invalid mpn parameter.')


def validate_get_rqst_parameter_region(get_rqst_params, validated_params, rqst_errors):
    if 'region' in get_rqst_params:
        validated_params['region'] = get_rqst_params['region']
        validated_params['region list'] = re.findall(r"[@\w. '-]+", validated_params['region'])

        if not validated_params['region list']:
            rqst_errors.append('Invalid region, regions must be ascii strings.')


def validate_get_rqst_parameter_location(get_rqst_params, validated_params, rqst_errors):
    if 'location' in get_rqst_params:
        validated_params['location'] = urllib.parse.unquote(get_rqst_params['location'])


def validate_get_rqst_parameter_locationid(get_rqst_params, validated_params, rqst_errors):
    if 'location_id' in get_rqst_params:
        validated_params['location_id'] = get_rqst_params['location_id']

        list_of_ids = re.findall("\d+", validated_params['location_id'])
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        validated_params['location_id list'] = list_of_ids

        if not validated_params['location_id list']:
            rqst_errors.append('Invalid location_id, ids must be base 10 integers')


def validate_get_rqst_parameter_navid(get_rqst_params, validated_params, rqst_errors):
    if 'navid' in get_rqst_params:
        validated_params['navigator id'] = get_rqst_params['navid']

        list_of_nav_ids = re.findall("\d+", validated_params['navigator id'])
        for indx, element in enumerate(list_of_nav_ids):
            list_of_nav_ids[indx] = int(element)
        validated_params['navigator id list'] = list_of_nav_ids

        if not validated_params['navigator id list']:
            rqst_errors.append('Invalid navigator id, navigator ids must be base 10 integers')


def validate_get_rqst_parameter_county(get_rqst_params, validated_params, rqst_errors):
    if "county" in get_rqst_params:
        validated_params['county'] = get_rqst_params['county']
        validated_params['county list'] = re.findall(r"[\w. '-]+", validated_params['county'])

        if not validated_params['county list']:
            rqst_errors.append('Invalid county parameter, county parameters must be ascii strings.')


def validate_get_rqst_parameter_zipcode(get_rqst_params, validated_params, rqst_errors):
    if "zipcode" in get_rqst_params:
        validated_params['zipcode'] = get_rqst_params['zipcode']
        validated_params['zipcode list'] = re.findall(r"\d+", validated_params['zipcode'])

        if not validated_params['zipcode list']:
            rqst_errors.append('Invalid zipcode, zipcodes must be integers')


def validate_get_rqst_parameter_time(get_rqst_params, validated_params, rqst_errors):
    if "time" in get_rqst_params:
        try:
            validated_params['look up date'] = datetime.date.today() - datetime.timedelta(days=int(get_rqst_params['time']))
            validated_params['time'] = get_rqst_params['time']
        except ValueError:
            rqst_errors.append('time parameter must be a valid integer.')


def validate_get_rqst_parameter_startdate(get_rqst_params, validated_params, rqst_errors):
    if "startdate" in get_rqst_params:
        try:
            datetime.datetime.strptime(get_rqst_params["startdate"], '%Y-%m-%d')
            validated_params['start date'] = get_rqst_params["startdate"]
        except ValueError:
            rqst_errors.append('startdate parameter must be a valid date.')


def validate_get_rqst_parameter_enddate(get_rqst_params, validated_params, rqst_errors):
    if "enddate" in get_rqst_params:
        try:
            datetime.datetime.strptime(get_rqst_params["enddate"], '%Y-%m-%d')
            validated_params['end date'] = get_rqst_params["enddate"]
        except ValueError:
            rqst_errors.append('enddate parameter must be a valid integer.')


def validate_get_rqst_parameter_is_cps_consumer(get_rqst_params, validated_params, rqst_errors):
    if 'is_cps_consumer' in get_rqst_params:
        validated_params['is_cps_consumer'] = get_rqst_params['is_cps_consumer'].lower()
        if validated_params['is_cps_consumer'] not in ('true', 'false'):
            rqst_errors.append("Value for is_cps_consumer is not type boolean")
        else:
            validated_params['is_cps_consumer'] = validated_params['is_cps_consumer'] in ('true')


def validate_get_rqst_parameter_partnerid(get_rqst_params, validated_params, rqst_errors):
    if 'partnerid' in get_rqst_params:
        validated_params['partnerid'] = get_rqst_params['partnerid']
        list_of_ids = re.findall("[@\w. '-_]+", validated_params['partnerid'])
        validated_params['partnerid list'] = list_of_ids

        if not validated_params['partnerid list']:
            rqst_errors.append('Invalid partnerid parameter, partnerid parameters must be ascii strings.')


def validate_get_rqst_parameter_fields(get_rqst_params, validated_params, rqst_errors):
    if 'fields' in get_rqst_params:
        validated_params['fields'] = urllib.parse.unquote(get_rqst_params['fields'])
        validated_params['fields list'] = re.findall(r"[@\w. '-]+", validated_params['fields'])

        if not validated_params['fields list']:
            rqst_errors.append('Invalid fields parameter, field parameters must be ascii strings.')


def validate_get_rqst_parameter_page(get_rqst_params, validated_params, rqst_errors):
    if 'page' in get_rqst_params:
        validated_params['page number'] = int(get_rqst_params['page'])


def validate_get_rqst_parameter_groupby(get_rqst_params, validated_params, rqst_errors):
    if "groupby" in get_rqst_params:
        validated_params['group by'] = get_rqst_params['groupby']


def validate_get_rqst_parameter_nav_location_tags(get_rqst_params, validated_params, rqst_errors):
    if 'nav_location_tags' in get_rqst_params:
        validated_params['nav_location_tags'] = get_rqst_params['nav_location_tags']
        validated_params['nav_location_tags list'] = re.findall(r"[@\w. '-]+", validated_params['nav_location_tags'])

        if not validated_params['nav_location_tags list']:
            rqst_errors.append('Invalid nav_location_tags parameter, nav_location_tags parameters must be ascii strings.')


def validate_get_rqst_parameter_is_cps_location(get_rqst_params, validated_params, rqst_errors):
    if 'is_cps_location' in get_rqst_params:
        validated_params['is_cps_location'] = get_rqst_params['is_cps_location'].lower()
        if validated_params['is_cps_location'] not in ('true', 'false'):
            rqst_errors.append("Value for is_cps_location is not type boolean")
        else:
            validated_params['is_cps_location'] = validated_params['is_cps_location'] in ('true')


def validate_get_rqst_parameter_name(get_rqst_params, validated_params, rqst_errors):
    if 'name' in get_rqst_params:
        validated_params['name'] = urllib.parse.unquote(get_rqst_params['name'])


def validate_get_rqst_parameter_intent(get_rqst_params, validated_params, rqst_errors):
    if 'intent' in get_rqst_params:
        validated_params['intent'] = urllib.parse.unquote(get_rqst_params['intent'])


def validate_get_rqst_parameter_state(get_rqst_params, validated_params, rqst_errors):
    if "state" in get_rqst_params:
        validated_params['state'] = get_rqst_params['state']
        validated_params['state list'] = re.findall(r"[\w. '-]+", validated_params['state'])

        number_of_commas = len(re.findall(r",", validated_params['state']))
        number_of_parameters_there_should_be = number_of_commas + 1
        if number_of_parameters_there_should_be != len(validated_params['state list']):
            rqst_errors.append('List of states is formatted wrong. Values must be ascii strings separated by commas')

        if not validated_params['state list']:
            rqst_errors.append('Invalid state, states must be ascii strings.')


def validate_get_rqst_parameter_has_sample_id_card(get_rqst_params, validated_params, rqst_errors):
    if 'has_sample_id_card' in get_rqst_params:
        validated_params['has_sample_id_card'] = get_rqst_params['has_sample_id_card'].lower()
        if validated_params['has_sample_id_card'] not in ('true', 'false'):
            rqst_errors.append("Value for has_sample_id_card is not type boolean")
        else:
            validated_params['has_sample_id_card'] = validated_params['has_sample_id_card'] in ('true')


def validate_get_rqst_parameter_carrier_id(get_rqst_params, validated_params, rqst_errors):
    if 'carrier_id' in get_rqst_params:
        validated_params['carrier id'] = get_rqst_params['carrier_id']

        list_of_carrier_ids = re.findall("\d+", validated_params['carrier id'])
        for indx, element in enumerate(list_of_carrier_ids):
            list_of_carrier_ids[indx] = int(element)
        validated_params['carrier id list'] = list_of_carrier_ids

        if not validated_params['carrier id list']:
            rqst_errors.append('Invalid carrier id, carrier ids must be base 10 integers')


def validate_get_rqst_parameter_carrier_state(get_rqst_params, validated_params, rqst_errors):
    if "carrier_state" in get_rqst_params:
        validated_params['carrier state'] = get_rqst_params['carrier_state']
        validated_params['carrier state list'] = re.findall(r"[\w. '-]+", validated_params['carrier state'])

        if not validated_params['carrier state list']:
            rqst_errors.append('Invalid carrier state, carrier states must be ascii strings.')


def validate_get_rqst_parameter_carrier_name(get_rqst_params, validated_params, rqst_errors):
    if 'carrier_name' in get_rqst_params:
        validated_params['carrier name'] = urllib.parse.unquote(get_rqst_params['carrier_name'])


def validate_get_rqst_parameter_accepted_location_id(get_rqst_params, validated_params, rqst_errors):
    if 'accepted_location_id' in get_rqst_params:
        validated_params['accepted_location_id'] = get_rqst_params['accepted_location_id']

        list_of_accepted_location_ids = re.findall("\d+", validated_params['accepted_location_id'])
        for indx, element in enumerate(list_of_accepted_location_ids):
            list_of_accepted_location_ids[indx] = int(element)
        validated_params['accepted_location_id_list'] = list_of_accepted_location_ids

        if not validated_params['accepted_location_id_list']:
            rqst_errors.append('Invalid accepted_location id, accepted_location ids must be base 10 integers')


def validate_get_rqst_parameter_network_name(get_rqst_params, validated_params, rqst_errors):
    if 'network_name' in get_rqst_params:
        validated_params['network_name'] = urllib.parse.unquote(get_rqst_params['network_name'])


def validate_get_rqst_parameter_network_id(get_rqst_params, validated_params, rqst_errors):
    if 'network_id' in get_rqst_params:
        validated_params['network_id'] = get_rqst_params['network_id']

        list_of_network_ids = re.findall("\d+", validated_params['network_id'])
        for indx, element in enumerate(list_of_network_ids):
            list_of_network_ids[indx] = int(element)
        validated_params['network_id_list'] = list_of_network_ids

        if not validated_params['network_id_list']:
            rqst_errors.append('Invalid network id, network ids must be base 10 integers')


def validate_get_rqst_parameter_premium_type(get_rqst_params, validated_params, rqst_errors):
    if 'premium_type' in get_rqst_params:
        validated_params['premium_type'] = get_rqst_params['premium_type']
        validated_params['premium_type list'] = re.findall(r"[@\w. '-]+", validated_params['premium_type'])

        if not validated_params['premium_type list']:
            rqst_errors.append('Invalid premium_type.')
        else:
            for premium_type in validated_params['premium_type list']:
                dummy_plan_object = HealthcarePlan(premium_type=premium_type)
                if not dummy_plan_object.check_premium_choices():
                    rqst_errors.append('The following is an invalid premium_type : {}'.format(premium_type))


def validate_get_rqst_parameter_include_summary_report(get_rqst_params, validated_params, rqst_errors):
    if 'include_summary_report' in get_rqst_params:
        validated_params['include_summary_report'] = get_rqst_params['include_summary_report'].lower()
        if validated_params['include_summary_report'] not in ('true', 'false'):
            rqst_errors.append("Value for include_summary_report is not type boolean")
        else:
            validated_params['include_summary_report'] = validated_params['include_summary_report'] in ('true')


def validate_get_rqst_parameter_include_detailed_report(get_rqst_params, validated_params, rqst_errors):
    if 'include_detailed_report' in get_rqst_params:
        validated_params['include_detailed_report'] = get_rqst_params['include_detailed_report'].lower()
        if validated_params['include_detailed_report'] not in ('true', 'false'):
            rqst_errors.append("Value for include_detailed_report is not type boolean")
        else:
            validated_params['include_detailed_report'] = validated_params['include_detailed_report'] in ('true')


def validate_get_rqst_parameter_question(get_rqst_params, validated_params, rqst_errors):
    if 'question' in get_rqst_params:
        validated_params['question'] = urllib.parse.unquote(get_rqst_params['question'])


def validate_get_rqst_parameter_gen_concern_name(get_rqst_params, validated_params, rqst_errors):
    if 'gen_concern_name' in get_rqst_params:
        validated_params['gen_concern_name'] = urllib.parse.unquote(get_rqst_params['gen_concern_name'])


def validate_get_rqst_parameter_gen_concern_id(get_rqst_params, validated_params, rqst_errors):
    if 'gen_concern_id' in get_rqst_params:
        validated_params['gen_concern_id'] = get_rqst_params['gen_concern_id']

        list_of_gen_concern_ids = re.findall("\d+", validated_params['gen_concern_id'])
        for indx, element in enumerate(list_of_gen_concern_ids):
            list_of_gen_concern_ids[indx] = int(element)
        validated_params['gen_concern_id_list'] = list_of_gen_concern_ids

        if not validated_params['gen_concern_id_list']:
            rqst_errors.append('Invalid gen_concern id, gen_concern ids must be base 10 integers')


def validate_get_rqst_parameter_gen_concern_id_subset(get_rqst_params, validated_params, rqst_errors):
    if 'gen_concern_id_subset' in get_rqst_params:
        validated_params['gen_concern_id_subset'] = get_rqst_params['gen_concern_id_subset']

        list_of_gen_concern_ids = re.findall("\d+", validated_params['gen_concern_id_subset'])
        for indx, element in enumerate(list_of_gen_concern_ids):
            list_of_gen_concern_ids[indx] = int(element)
        validated_params['gen_concern_id_subset_list'] = list_of_gen_concern_ids

        if not validated_params['gen_concern_id_subset_list']:
            rqst_errors.append('Invalid gen_concern id, gen_concern ids must be base 10 integers')


def validate_get_rqst_parameter_hospital_name(get_rqst_params, validated_params, rqst_errors):
    if 'hospital_name' in get_rqst_params:
        validated_params['hospital_name'] = urllib.parse.unquote(get_rqst_params['hospital_name'])


def validate_get_rqst_parameter_family_size(get_rqst_params, validated_params, rqst_errors):
    if 'family_size' in get_rqst_params:
        validated_params['family_size'] = get_rqst_params['family_size']

        list_of_family_sizes = re.findall("\d+", validated_params['family_size'])
        for indx, element in enumerate(list_of_family_sizes):
            list_of_family_sizes[indx] = int(element)
        validated_params['family_size_list'] = list_of_family_sizes

        if not validated_params['family_size_list']:
            rqst_errors.append('Invalid family_size, family_sizes must be base 10 integers')


class HTTPParameterValidatorBase:
    parameter_name = None

    def validate_get_rqst_parameter(self, get_rqst_params, validated_params, rqst_errors):
        if self.parameter_name:
            pass
        else:
            raise NotImplementedError("self.parameter_name must be set to a non null value in order to use this function.")


GET_PARAMETER_VALIDATION_FUNCTIONS = {
    "id": validate_get_rqst_parameter_id,
    "fname": validate_get_rqst_parameter_fname,
    "lname": validate_get_rqst_parameter_lname,
    "email": validate_get_rqst_parameter_email,
    "name": validate_get_rqst_parameter_name,
    "navid": validate_get_rqst_parameter_navid,

    "mpn": validate_get_rqst_parameter_mpn,
    "region": validate_get_rqst_parameter_region,
    "location": validate_get_rqst_parameter_location,
    "location_id": validate_get_rqst_parameter_locationid,
    "nav_location_tags": validate_get_rqst_parameter_nav_location_tags,
    "is_cps_location": validate_get_rqst_parameter_is_cps_location,

    "county": validate_get_rqst_parameter_county,
    "zipcode": validate_get_rqst_parameter_zipcode,
    "time": validate_get_rqst_parameter_time,
    "startdate": validate_get_rqst_parameter_startdate,
    "enddate": validate_get_rqst_parameter_enddate,
    "is_cps_consumer": validate_get_rqst_parameter_is_cps_consumer,

    "partnerid": validate_get_rqst_parameter_partnerid,
    "intent": validate_get_rqst_parameter_intent,

    "state": validate_get_rqst_parameter_state,
    "has_sample_id_card": validate_get_rqst_parameter_has_sample_id_card,

    "carrier_id": validate_get_rqst_parameter_carrier_id,
    "carrier_state": validate_get_rqst_parameter_carrier_state,
    "carrier_name": validate_get_rqst_parameter_carrier_name,
    'accepted_location_id': validate_get_rqst_parameter_accepted_location_id,
    "network_name": validate_get_rqst_parameter_network_name,
    "network_id": validate_get_rqst_parameter_network_id,
    "premium_type": validate_get_rqst_parameter_premium_type,
    "include_summary_report": validate_get_rqst_parameter_include_summary_report,
    "include_detailed_report": validate_get_rqst_parameter_include_detailed_report,

    "question": validate_get_rqst_parameter_question,
    "gen_concern_name": validate_get_rqst_parameter_gen_concern_name,
    "gen_concern_id": validate_get_rqst_parameter_gen_concern_id,
    "gen_concern_id_subset": validate_get_rqst_parameter_gen_concern_id_subset,

    "hospital_name": validate_get_rqst_parameter_hospital_name,

    "family_size": validate_get_rqst_parameter_family_size,

    'fields': validate_get_rqst_parameter_fields,
    "page": validate_get_rqst_parameter_page,
    "groupby": validate_get_rqst_parameter_groupby,
}