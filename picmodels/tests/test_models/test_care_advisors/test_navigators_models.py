import datetime

from django.test import TestCase

from picmodels.tests.test_models.base import DBModelsBaseTestCase

from picmodels.models import Navigators


class NavigatorsTestCase(DBModelsBaseTestCase, TestCase):
    db_model = Navigators
    validated_params = {
        "first_name": "Hitsugaya",
        "last_name": "Toshiro",
        "email": "ksf@lis.com",
        "type": "Navigator",
        "county": 'Cook',
        "mpn": "12984892137",
        "add_base_locations": [
            "Presence Holy Family Medical Center"
        ],
        # "remove_base_locations": [
        #     # "",
        #     #  "ksjdh"
        # ],

        'add_healthcare_locations_worked': [
            {
                'name': 'Edward Hospital & Immediate Careasdss',
                'state_province': 'not available'
            }
        ],
        # 'remove_healthcare_locations_worked': [
        #     {
        #         'name': 'Edward Hospital & Immediate Careasdss',
        #         'state_province': 'not available'
        #     }
        # ],
        'add_healthcare_service_expertises': [
            'bariatrics',
        ],
        # 'remove_healthcare_service_expertises': [
        #     'bariatrics',
        # ],
        'add_insurance_carrier_specialties': [
            {
                'name': 'Health Alliance Medical Plans, Inc.',
                'state_province': 'il'
            },
        ],
        # 'remove_insurance_carrier_specialties': [
        #     {
        #         'name': 'Health Alliance Medical Plans, Inc.',
        #         'state_province': 'il'
        #     },
        # ],

        "create_resume_row": {
            "profile_description": "apple",
            "create_education_rows": [
                {
                    "school": "easy",
                    "major": "peasy",
                    "degree_type": "masters"
                },
                {
                    "school": "lemon",
                    "major": "squeezy",
                    "degree_type": "masters"
                },
            ],
            "create_job_rows": [
                {
                    "title": "easy",
                    "company": "peasy",
                    "description": "masters"
                },
                {
                    "title": "lemon",
                    "company": "squeezy",
                    "description": "masters"
                },
            ],
        },

        "address_line_1": "",
        "address_line_2": "",
        "city": "",
        "state_province": "",
        "zipcode": "",

        "phone": "2813307004",
        "reported_region": "cook",
        "video_link": "https://www.twitch.tv/videos/239858398",
        "navigator_organization": "aijsaid",

        "db_action": "create",
    }

    def test_create_row_w_validated_params(self):
        test_errors = []

        db_row = self.use_create_row_w_validated_params(
            self.validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.first_name,
                self.validated_params['first_name'],
                "row name: {}, request name: {}".format(db_row.first_name, self.validated_params['first_name'])
            )
            self.assertEqual(
                db_row.navigator_organization,
                self.validated_params['navigator_organization'],
                "row name: {}, request name: {}".format(db_row.navigator_organization, self.validated_params['navigator_organization'])
            )
            self.assertEqual(
                len(db_row.base_locations.all()),
                1,
                "row base locations count: {}".format(len(db_row.base_locations.all()))
            )
            self.assertEqual(
                len(db_row.healthcare_locations_worked.all()),
                1,
                "row healthcare_locations_worked count: {}".format(len(db_row.healthcare_locations_worked.all()))
            )
            self.assertEqual(
                len(db_row.insurance_carrier_specialties.all()),
                1,
                "row insurance_carrier_specialties count: {}".format(len(db_row.insurance_carrier_specialties.all()))
            )
            self.assertEqual(
                len(db_row.healthcare_service_expertises.all()),
                1,
                "row healthcare_service_expertises count: {}".format(len(db_row.healthcare_service_expertises.all()))
            )
            self.assertEqual(
                len(db_row.resume_set.all()),
                1,
                "row resume count: {}".format(len(db_row.resume_set.all()))
            )

    def test_update_row_w_validated_params(self):
        self.validated_params["first_name"] = "Hitsugayasdasa"
        self.validated_params["last_name"] = "Toshiro"
        self.validated_params["email"] = "ksf@lis.com"
        self.validated_params["type"] = "Navigator"
        self.validated_params["county"] = 'Cook'
        self.validated_params["mpn"] = "12984892137"

        # self.validated_params["add_base_locations"] = [
        #     "Presence Holy Family Medical Center"
        # ]
        del self.validated_params["add_base_locations"]
        self.validated_params["remove_base_locations"] = [
            "Illinois Department of Employment Security- Lawrence"
        ]

        # self.validated_params['add_healthcare_locations_worked'] = [
        #     {
        #         'name': 'Edward Hospital & Immediate Careasdss',
        #         'state_province': 'not available'
        #     }
        # ]
        del self.validated_params['add_healthcare_locations_worked']
        self.validated_params['remove_healthcare_locations_worked'] = [
            {
                'name': 'Edward Hospital & Immediate Careasdss',
                'state_province': 'not available'
            }
        ]

        # self.validated_params['add_healthcare_service_expertises'] = [
        #     'bariatrics',
        # ],
        del self.validated_params['add_healthcare_service_expertises']
        self.validated_params['remove_healthcare_service_expertises'] = [
            'bariatrics',
        ]

        # self.validated_params['add_insurance_carrier_specialties'] = [
        #     {
        #         'name': 'Health Alliance Medical Plans, Inc.',
        #         'state_province': 'il'
        #     },
        # ]
        del self.validated_params['add_insurance_carrier_specialties']
        self.validated_params['remove_insurance_carrier_specialties'] = [
            {
                'name': 'Health Alliance Medical Plans, Inc.',
                'state_province': 'il'
            },
        ]

        # self.validated_params["create_resume_row"] = {
        #     "profile_description": "apple",
        #     "create_education_rows": [
        #         {
        #             "school": "easy",
        #             "major": "peasy",
        #             "degree_type": "masters"
        #         },
        #         {
        #             "school": "lemon",
        #             "major": "squeezy",
        #             "degree_type": "masters"
        #         },
        #     ],
        #     "create_job_rows": [
        #         {
        #             "title": "easy",
        #             "company": "peasy",
        #             "description": "masters"
        #         },
        #         {
        #             "title": "lemon",
        #             "company": "squeezy",
        #             "description": "masters"
        #         },
        #     ],
        # }
        # self.validated_params["update_resume_row"] = {
        #     "profile_description": "applesauce",
        #     # "create_education_rows": [
        #     #     {
        #     #         "school": "easy",
        #     #         "major": "peasy",
        #     #         "degree_type": "masters"
        #     #     },
        #     #     {
        #     #         "school": "lemon",
        #     #         "major": "squeezy",
        #     #         "degree_type": "masters"
        #     #     },
        #     # ],
        #     # "update_education_rows": [
        #     #     {
        #     #         "school": "easy",
        #     #         "major": "peasy",
        #     #         "degree_type": "bachelors",
        #     #         "id": 4,
        #     #     },
        #     #     {
        #     #         "school": "lemon",
        #     #         "major": "squeezy",
        #     #         "degree_type": "masters",
        #     #         "id": 3,
        #     #     },
        #     # ],
        #     "delete_education_rows": [
        #         {
        #             "id": 4,
        #         },
        #         {
        #             "id": 3,
        #         },
        #     ],
        #
        #     # "create_job_rows": [
        #     #     {
        #     #         "title": "easy",
        #     #         "company": "peasy",
        #     #         "description": "masters"
        #     #     },
        #     #     {
        #     #         "title": "lemon",
        #     #         "company": "squeezy",
        #     #         "description": "masters"
        #     #     },
        #     # ],
        #     # "update_job_rows": [
        #     #     {
        #     #         "title": "easy",
        #     #         "company": "peasy",
        #     #         "description": "question",
        #     #         "id": 4,
        #     #     },
        #     #     {
        #     #         "title": "lemon",
        #     #         "company": "squeezy",
        #     #         "description": "blind",
        #     #         "id": 3,
        #     #     },
        #     # ],
        #     "delete_job_rows": [
        #         {
        #             "id": 4,
        #         },
        #         {
        #             "id": 3,
        #         },
        #     ],
        #     "id": 6,
        # },
        del self.validated_params["create_resume_row"]
        self.validated_params["delete_resume_row"] = {
            "id": 6,
        }

        self.validated_params["address_line_1"] = ""
        self.validated_params["address_line_2"] = ""
        self.validated_params["city"] = ""
        self.validated_params["state_province"] = ""
        self.validated_params["zipcode"] = ""

        self.validated_params["phone"] = "2813307004"
        self.validated_params["reported_region"] = "cook"
        self.validated_params["video_link"] = "https://www.twitch.tv/videos/239858398"

        self.validated_params["db_action"] = "update"
        self.validated_params["id"] = 59

        test_errors = []

        db_row = self.use_update_row_w_validated_params(
            self.validated_params,
            test_errors
        )

        if db_row:
            self.assertEqual(
                db_row.first_name,
                self.validated_params['first_name'],
                "row name: {}, request name: {}".format(db_row.first_name, self.validated_params['first_name'])
            )
            self.assertEqual(
                db_row.navigator_organization,
                self.validated_params['navigator_organization'],
                "row name: {}, request name: {}".format(db_row.navigator_organization,
                                                        self.validated_params['navigator_organization'])
            )
            self.assertEqual(
                len(db_row.base_locations.all()),
                0,
                "row base locations count: {}".format(len(db_row.base_locations.all()))
            )
            self.assertEqual(
                len(db_row.healthcare_locations_worked.all()),
                0,
                "row healthcare_locations_worked count: {}".format(len(db_row.healthcare_locations_worked.all()))
            )
            self.assertEqual(
                len(db_row.insurance_carrier_specialties.all()),
                0,
                "row insurance_carrier_specialties count: {}".format(len(db_row.insurance_carrier_specialties.all()))
            )
            self.assertEqual(
                len(db_row.healthcare_service_expertises.all()),
                0,
                "row healthcare_service_expertises count: {}".format(len(db_row.healthcare_service_expertises.all()))
            )
            self.assertEqual(
                len(db_row.resume_set.all()),
                0,
                "row resume count: {}".format(len(db_row.resume_set.all()))
            )

    def test_delete_row_w_validated_params(self):
        self.validated_params["id"] = 4
        self.validated_params["db_action"] = "delete"

        test_errors = []

        self.use_delete_row_w_validated_params(
            self.validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_id(self):
        validated_params = {
            "id_list": [1],
            "id": u"1"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_id(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_first_name(self):
        validated_params = {
            "first_name_list": ['bradley'],
            "first_name": u"bradley"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_first_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_last_name(self):
        validated_params = {
            "last_name_list": ['awodu'],
            "last_name": u"awodu"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_last_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_f_and_l_name(self):
        validated_params = {
            "first_name_list": ['bradley'],
            "first_name": u"bradley",
            "last_name_list": ['awodu'],
            "last_name": u"awodu"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_f_and_l_name(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_email(self):
        validated_params = {
            "email_list": ['tech@piccares.org'],
            "email": u"tech@piccares.org"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_email(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_county(self):
        validated_params = {
            "county_list": ['Cook'],
            "county": u"Cook"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_county(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_region(self):
        validated_params = {
            "region_list": ['1'],
            "region": u"1"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_region(
            validated_params,
            test_errors
        )

    def test_get_serialized_rows_by_mpn(self):
        validated_params = {
            "mpn_list": ['17074248'],
            "mpn": u"17074248"
        }

        test_errors = []

        serialized_table_data = self.use_get_serialized_rows_by_mpn(
            validated_params,
            test_errors
        )
