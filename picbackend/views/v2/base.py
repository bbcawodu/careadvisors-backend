"""
Defines views that handle Patient Innovation Center consumer based requests
API Version 2
"""

from django.http import HttpResponse
import json
from .utils import build_search_params
from .utils import init_v2_response_data
from .utils import parse_and_log_errors


class JSONGETRspMixin(object):
    get_logic_function = None

    def get(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center GET requests that return json objects in the body
        :param request: django request instance object
        :rtype: HttpResponse
        """

        if self.get_logic_function:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, rqst_errors = init_v2_response_data()

            # Build dictionary that contains valid Patient Innovation Center GET parameters
            search_params = build_search_params(request.GET, rqst_errors)

            response_raw_data, rqst_errors = self.get_logic_function(request, search_params, response_raw_data, rqst_errors)

            response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response


class JSONPOSTRspMixin(object):
    post_logic_function = None

    def post(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center POST requests that accept and return json objects in the body
        :param request: django request instance object
        :rtype: HttpResponse
        """

        if self.post_logic_function:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, post_errors = init_v2_response_data()

            post_json = request.body.decode('utf-8')
            post_data = json.loads(post_json)

            response_raw_data, post_errors = self.post_logic_function(post_data, response_raw_data, post_errors)

            response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response


class JSONPUTRspMixin(object):
    put_logic_function = None

    def put(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center PUT requests that accept and return json objects in the body
        :param request: django request instance object
        :rtype: HttpResponse
        """

        if self.put_logic_function:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, post_errors = init_v2_response_data()

            post_json = request.body.decode('utf-8')
            post_data = json.loads(post_json)

            response_raw_data, post_errors = self.put_logic_function(post_data, response_raw_data, post_errors)

            response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response


class JSONDELETERspMixin(object):
    delete_logic_function = None

    def delete(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center DELETE requests that accept and return json objects in the body
        :param request: django request instance object
        :rtype: HttpResponse
        """

        if self.delete_logic_function:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, post_errors = init_v2_response_data()

            post_json = request.body.decode('utf-8')
            post_data = json.loads(post_json)

            response_raw_data, post_errors = self.delete_logic_function(post_data, response_raw_data, post_errors)

            response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response


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

