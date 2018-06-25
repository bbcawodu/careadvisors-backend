import datetime
from django.test import TestCase

from picbackend.views.utils.get_parameter_validation_functions import GET_PARAMETER_VALIDATION_FUNCTIONS


class GetRqstParamValidationTestCase(TestCase):
    def test_get_rqst_param_validation(self):
        for param_name, validation_dict in GET_PARAMETER_VALIDATION_FUNCTIONS.items():
            param_type = validation_dict['type']
            validation_function = validation_dict['function']
            errors_list = []
            validated_params = {}

            if param_type == 'int_with_all':
                unvalidated_params = {
                    param_name: "1,2,3"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params['{}_list'.format(param_name)],
                    [1,2,3]
                )

                errors_list = []
                validated_params = {}
                unvalidated_params = {
                    param_name: "all"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params[param_name],
                    'all'
                )
            elif param_type == 'int':
                unvalidated_params = {
                    param_name: "1,2,3"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params['{}_list'.format(param_name)],
                    [1, 2, 3]
                )
            elif param_type == 'single_int':
                unvalidated_params = {
                    param_name: "1"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params[param_name],
                    1
                )
            elif param_type == 'time_delta_in_days':
                unvalidated_params = {
                    param_name: "1"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params[param_name],
                    datetime.timedelta(days=1)
                )
            elif param_type == 'string':
                unvalidated_params = {
                    param_name: "apple,martini,sauce"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params['{}_list'.format(param_name)],
                    ['apple', 'martini', 'sauce']
                )
            elif param_type == 'url_encoded_string':
                unvalidated_params = {
                    param_name: "charlie%20and%20the%20chocolate%20factory"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params[param_name],
                    "charlie and the chocolate factory"
                )
            elif param_type == 'date_string':
                unvalidated_params = {
                    param_name: "2018-06-30"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params[param_name].day,
                    30
                )
                self.assertEqual(
                    validated_params[param_name].month,
                    6
                )
                self.assertEqual(
                    validated_params[param_name].year,
                    2018
                )
            elif param_type == 'bool_string':
                unvalidated_params = {
                    param_name: "true"
                }
                validation_function(unvalidated_params, validated_params, errors_list)
                self.assertEqual(
                    len(errors_list),
                    0,
                    "param_name: {}, given params: {}, errors_list: {}".format(
                        param_name, unvalidated_params, errors_list
                    )
                )
                self.assertEqual(
                    validated_params[param_name],
                    True
                )
