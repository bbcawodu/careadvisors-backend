import datetime
import re
import urllib
from picmodels.models import HealthcarePlan


def validate_get_rqst_parameter_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        if validated_params[param_name] != "all":
            validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_first_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'first_name'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_last_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'last_name'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_email(get_rqst_params, validated_params, rqst_errors):
    param_name = 'email'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_mpn(get_rqst_params, validated_params, rqst_errors):
    param_name = 'mpn'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_region(get_rqst_params, validated_params, rqst_errors):
    param_name = 'region'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_location(get_rqst_params, validated_params, rqst_errors):
    if 'location' in get_rqst_params:
        validated_params['location'] = urllib.parse.unquote(get_rqst_params['location'])


def validate_get_rqst_parameter_locationid(get_rqst_params, validated_params, rqst_errors):
    param_name = 'location_id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_nav_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'nav_id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_county(get_rqst_params, validated_params, rqst_errors):
    param_name = 'county'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_zipcode(get_rqst_params, validated_params, rqst_errors):
    param_name = "zipcode"

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


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


def validate_get_rqst_parameter_partner_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'partner_id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_fields(get_rqst_params, validated_params, rqst_errors):
    if 'fields' in get_rqst_params:
        validated_params['fields'] = urllib.parse.unquote(get_rqst_params['fields'])
        validated_params['fields list'] = re.findall(r"[@\w. '-]+", validated_params['fields'])

        if not validated_params['fields list']:
            rqst_errors.append('Invalid fields parameter, field parameters must be ascii strings.')


def validate_get_rqst_parameter_page(get_rqst_params, validated_params, rqst_errors):
    param_name = 'page'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_groupby(get_rqst_params, validated_params, rqst_errors):
    if "groupby" in get_rqst_params:
        validated_params['group by'] = get_rqst_params['groupby']


def validate_get_rqst_parameter_nav_location_tags(get_rqst_params, validated_params, rqst_errors):
    param_name = 'nav_location_tags'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


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
    param_name = "state"

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_has_sample_id_card(get_rqst_params, validated_params, rqst_errors):
    if 'has_sample_id_card' in get_rqst_params:
        validated_params['has_sample_id_card'] = get_rqst_params['has_sample_id_card'].lower()
        if validated_params['has_sample_id_card'] not in ('true', 'false'):
            rqst_errors.append("Value for has_sample_id_card is not type boolean")
        else:
            validated_params['has_sample_id_card'] = validated_params['has_sample_id_card'] in ('true')


def validate_get_rqst_parameter_carrier_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'carrier_id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


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
    param_name = 'accepted_location_id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_network_name(get_rqst_params, validated_params, rqst_errors):
    if 'network_name' in get_rqst_params:
        validated_params['network_name'] = urllib.parse.unquote(get_rqst_params['network_name'])


def validate_get_rqst_parameter_network_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'network_id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


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
    param_name = 'gen_concern_id'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_gen_concern_id_subset(get_rqst_params, validated_params, rqst_errors):
    param_name = 'gen_concern_id_subset'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_hospital_name(get_rqst_params, validated_params, rqst_errors):
    if 'hospital_name' in get_rqst_params:
        validated_params['hospital_name'] = urllib.parse.unquote(get_rqst_params['hospital_name'])


def validate_get_rqst_parameter_family_size(get_rqst_params, validated_params, rqst_errors):
    param_name = 'family_size'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value = unvalidated_param_value

    validated_params[param_name] = validated_param_value


def validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value_list = re.findall("\d+", unvalidated_param_value)
    for indx, element in enumerate(validated_param_value_list):
        validated_param_value_list[indx] = int(element)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    if not validated_param_value_list:
        rqst_errors.append('Invalid {}, {}s must be base 10 integers'.format(param_name, param_name))

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append(
            'List of {}s is formatted wrong. Values must be base 10 integers separated by commas'.format(param_name))


def validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value = unvalidated_param_value

    validated_params[param_name] = validated_param_value


def validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value_list = re.findall(r"[@\w. '-]+", unvalidated_param_value)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    if not validated_param_value_list:
        rqst_errors.append('Invalid {}, {}s must be ascii encoded strings.'.format(param_name, param_name))

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append('List of {}s is formatted wrong. Values must be ascii strings separated by commas'.format(param_name))


class HTTPParameterValidatorBase:
    parameter_name = None

    def validate_get_rqst_parameter(self, get_rqst_params, validated_params, rqst_errors):
        if self.parameter_name:
            pass
        else:
            raise NotImplementedError("self.parameter_name must be set to a non null value in order to use this function.")


GET_PARAMETER_VALIDATION_FUNCTIONS = {
    "id": validate_get_rqst_parameter_id,
    "first_name": validate_get_rqst_parameter_first_name,
    "last_name": validate_get_rqst_parameter_last_name,
    "email": validate_get_rqst_parameter_email,
    "name": validate_get_rqst_parameter_name,
    "nav_id": validate_get_rqst_parameter_nav_id,

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

    "partner_id": validate_get_rqst_parameter_partner_id,
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