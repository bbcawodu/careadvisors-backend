import sys
import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import connection
from django.conf import settings
from .get_parameter_validation_functions import GET_PARAMETER_VALIDATION_FUNCTIONS
from django.core.exceptions import PermissionDenied


def ajax_required_attr_method_wrapper(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required_attr_method_wrapper
    def my_view(request):
        ....

    """
    def wrap(self, request, *args, **kwargs):
            if not request.is_ajax():
                raise PermissionDenied()
            return f(self, request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


class JSONGETRspMixin(object):
    parse_GET_request_and_add_response = None
    accepted_GET_request_parameters = None

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(JSONGETRspMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.parse_GET_request_and_add_response is None:
            raise NotImplementedError("Need to set class attribute, 'parse_GET_request_and_add_response'.")
        elif self.accepted_GET_request_parameters is None:
            raise NotImplementedError("Need to set class attribute, 'accepted_parameters'. If no parameters are needed, set class attribute to an empty list.")
        else:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, rqst_errors = init_v2_response_data()

            # Build dictionary that contains valid Patient Innovation Center GET parameters
            validated_GET_rqst_params = validate_get_request_parameters(request.GET, self.accepted_GET_request_parameters, rqst_errors)

            if not rqst_errors:
                self.parse_GET_request_and_add_response(request, validated_GET_rqst_params, response_raw_data, rqst_errors)

            parse_and_log_errors(response_raw_data, rqst_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response


class JSONPOSTRspMixin(object):
    parse_POST_request_and_add_response = None

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(JSONPOSTRspMixin, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.parse_POST_request_and_add_response:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, rqst_errors = init_v2_response_data()

            json_encoded_rqst_body = request.body.decode('utf-8')
            rqst_body = json.loads(json_encoded_rqst_body)

            self.parse_POST_request_and_add_response(rqst_body, response_raw_data, rqst_errors)

            parse_and_log_errors(response_raw_data, rqst_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response
        else:
            raise NotImplementedError("Need to set class attribute, 'parse_POST_request_and_add_response'.")


class JSONPUTRspMixin(object):
    parse_PUT_request_and_add_response = None

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(JSONPUTRspMixin, self).dispatch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if self.parse_PUT_request_and_add_response:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, rqst_errors = init_v2_response_data()

            json_encoded_rqst_body = request.body.decode('utf-8')
            rqst_body = json.loads(json_encoded_rqst_body)

            self.parse_PUT_request_and_add_response(rqst_body, response_raw_data, rqst_errors)

            parse_and_log_errors(response_raw_data, rqst_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response
        else:
            raise NotImplementedError("Need to set class attribute, 'parse_PUT_request_and_add_response'.")


class JSONDELETERspMixin(object):
    parse_DELETE_request_and_add_response = None

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(JSONDELETERspMixin, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center DELETE requests that accept and return json objects in the body
        :param request: django request instance object
        :rtype: HttpResponse
        """

        if self.parse_DELETE_request_and_add_response:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, rqst_errors = init_v2_response_data()

            json_encoded_rqst_body = request.body.decode('utf-8')
            rqst_body = json.loads(json_encoded_rqst_body)

            self.parse_DELETE_request_and_add_response(rqst_body, response_raw_data, rqst_errors)

            parse_and_log_errors(response_raw_data, rqst_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response
        else:
            raise NotImplementedError("Need to set class attribute, 'parse_DELETE_request_and_add_response'.")


JSONGETRspMixin.get = ajax_required_attr_method_wrapper(JSONGETRspMixin.get)
JSONPUTRspMixin.put = ajax_required_attr_method_wrapper(JSONPUTRspMixin.put)
JSONPOSTRspMixin.post = ajax_required_attr_method_wrapper(JSONPOSTRspMixin.post)
JSONDELETERspMixin.delete = ajax_required_attr_method_wrapper(JSONDELETERspMixin.delete)


class JSONRspMixin(object):
    put_logic_function = None
    get_logic_function = None

    # def get_template(self):
    #     if self.template == '':
    #         raise ImproperlyConfigured(
    #             '"template" variable  not defined in %s'
    #             % self.__class__.__name__)
    #     return self.template
    #
    # def get_redirect_url(self,obj):
    #     if self.redirect:
    #         url = self.redirect
    #     else:
    #         try:
    #             url = obj.get_absolute_url()
    #         except AttributeError:
    #             raise ImproperlyConfigured(
    #                 '"redirect" variable must be defined '
    #                 'in %s when redirecting %s objects.'
    #                 % (self.__class__.__name__,
    #                    obj.__class__.__name__))
    #     return url
    #
    # def get(self, request):
    #     form = self.form()
    #     return render(request,
    #                   self.get_template(),
    #                   {'form': form})
    #
    # def post(self, request):
    #     form = self.form(request.POST)
    #     if form.is_valid():
    #         new_obj = form.save()
    #         return redirect(self.get_redirect_url(new_obj))
    #     else:
    #         return render(request,
    #                       self.get_template(),
    #                       {'form': form})


def clean_string_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, empty_string_allowed=False,
                                        none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the string value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get string from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param empty_string_allowed: (type: boolean) whether an empty string allowed for given key, default is False
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: string or None) String type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] == "" and empty_string_allowed is False:
        post_errors.append("Value for {!r} in {!r} object is an empty string".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and none_allowed is False:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], str):
        post_errors.append("Value for {!r} in {!r} object is not a string".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]


def clean_int_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the integer value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get integer from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: integer or None) Integer type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and not none_allowed:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], int):
        post_errors.append("Value for {!r} in {!r} object is not an integer".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]


def clean_float_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the float value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get integer from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: float or None) Integer type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and not none_allowed:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], float) and not isinstance(dict_object[dict_key], int):
        post_errors.append("Value for {!r} in {!r} object is not an float".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
    else:
        return float(dict_object[dict_key])


def clean_dict_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the dictionary value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get dictionary from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: dictionary or None) dictionary type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and none_allowed == False:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], dict):
        post_errors.append("Value for {!r} in {!r} object is not a dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] == {}:
        post_errors.append("Value for {!r} in {!r} object is an empty dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]
    return None


def clean_list_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, empty_list_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the list value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get list from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param empty_list_allowed: (type: boolean) whether an empty list is allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: list or None) list type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], list):
        post_errors.append("Value for {!r} in {!r} object is not a list".format(dict_key, dict_name))
    elif dict_object[dict_key] == []:
        if empty_list_allowed:
            return []
        else:
            post_errors.append("Value for {!r} in {!r} object is an empty list".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]
    return None


def clean_bool_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the boolean value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get boolean from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: boolean or None) boolean type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], bool):
        post_errors.append("Value for {!r} in {!r} object is not type boolean".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]


def validate_get_request_parameters(get_rqst_params, params_to_validate, rqst_errors):
    validated_params = {}

    def run_validation_functions():
        for parameter_to_validate in params_to_validate:
            if parameter_to_validate in GET_PARAMETER_VALIDATION_FUNCTIONS:
                validation_fucntion = GET_PARAMETER_VALIDATION_FUNCTIONS[parameter_to_validate]
                validation_fucntion(get_rqst_params, validated_params, rqst_errors)
            else:
                raise NotImplementedError("GET parameter :{} does not have a validation function implemented.".format(parameter_to_validate))

    run_validation_functions()

    return validated_params


def init_v2_response_data():
    """
    This function returns a skelleton dictionary that can be used for PIC JSON responses

    :return: (type: dictionary) dictionary that can be used in PIC JSON responses
    """
    return {'Status': {"Error Code": 0, "Warnings": [], "Version": 2.0, "Missing Parameters": []},
            'Data': {}}, []


def parse_and_log_errors(response_raw_data, errors_list):
    """
    This function takes a list of error messages, adds them to a PIC API response dictionary, and adds the
    correct error code

    :param response_raw_data: (type: dictionary) dictionary that can be used in PIC JSON responses
    :param errors_list: (type: list) list of error messages
    :return: (type: dictionary) dictionary that can be used in PIC JSON responses with errors logged
    """

    if settings.DEBUG:
        db_statements_made = connection.queries
        print(db_statements_made)
        sys.stdout.flush()

    if errors_list:
        if response_raw_data["Status"]["Error Code"] == 0:
            response_raw_data["Status"]["Error Code"] = 1
        response_raw_data["Status"]["Errors"] = errors_list

        for message in errors_list:
            print(message)
            sys.stdout.flush()
