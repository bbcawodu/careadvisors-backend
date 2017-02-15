## Pokitdok Backend API

### Pokitdok Trading Partner Retrieval API.
- To retrieve parsed trading partner data from pokitdok, submit a GET request to http://picbackend.herokuapp.com/v2/health_insurance_trading_partners/ with the following optional parameter: "partnerid"
    - "partnerid" corresponds to the partner id provided by pokitdok for a given trading partner.
        - If this parameter is provided, results will contain valid search parameters for eligibility checks.
    
    
- The response for requests WITHOUT partnerid provided will be a JSON document with the following format:
    ```
    {
        "Status": {
                    "Version": Integer,
                    "Error Code": Integer,
                    "Errors": Array
                  }
        "Data": {
                    {
                    "enrollment_required": [],
                    "restricted_transactions": [
                    "837"
                    ],
                    "supported_transactions": [
                    "837"
                    ],
                    "name": "8th District Electrical Benefit Fund",
                    "is_enabled": true,
                    "id": "8th_district_electrical"
                    },
                    {
                    "enrollment_required": [],
                    "restricted_transactions": [
                    "837"
                    ],
                    "supported_transactions": [
                    "837",
                    "270"
                    ],
                    "name": "AARP Medicare Complete",
                    "is_enabled": true,
                    "id": "aarp_medicare_complete"
                    },
    }
    ```
    
    
- The response for requests WITH partnerid provided will be a JSON document with the following format:
    ```
    {
        "Status": {
                    "Version": 2.0,
                    "Error Code": Integer,
                    "Errors": Array
                  }
        "Data": {
                    {
                    "enrollment_required": [],
                    "restricted_transactions": [
                    "837"
                    ],
                    "supported_transactions": [
                    "837"
                    ],
                    "name": "8th District Electrical Benefit Fund",
                    "is_enabled": true,
                    "id": "8th_district_electrical"
                    }
    }
    ```
    
    
    
### Pokitdok Eligibility Retrieval API.
- To retrieve parsed eligibility data from pokitdok for a consumer, submit a POST request to http://picbackend.herokuapp.com/v2/consumer_health_insurance_benefits/. 

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"Birth Date":"YYYY-MM-DD" (Can be None),
"First Name": String (Can be None),
"Last Name": String (Can be None),
"Gender": String (Can be None),
"Trading Partner ID": Plan name code which can be retrieved from trading partner API (String),
"Consumer Plan ID": String (Can be None)
}
```

- The consumer parameters ("Trading Partner ID" is mandatory) need to match patterns according to the trading partner you are requesting. Use /v1/tradingpartners?partnerid="Trading Partner ID" to retrieve valid paramater set:


    
- The response will be a JSON document with the following format:
    ```
    {
        "Status": {
                    "Version": 2.0,
                    "Error Code": Integer,
                    "Errors": Array
                  },
        "Pokitdok Raw Results": Dictionary object(Raw Pokitdok results for debug purposes),
        "Data": {
                    "Plan Start Date": "YYYY-MM-DD",
                    "Consumer Info": {
                                        "id": Plan ID number (String),
                                        "birth_date": "YYYY-MM-DD",
                                        "address": {
                                                        "state": "XX",
                                                        "address_lines": [
                                                                            String,
                                                                            ...
                                                                         ],
                                                        "zipcode": String,
                                                        "city": String
                                                    },
                                        "first_name": String,
                                        "last_name": String,
                                        "gender": String,
                                        "middle_name": String
                                     },
                    "Payer Info": {
                                        "id": Plan code (String),
                                        "name": Plan name (String),
                                     },
                    "Insurance Type": eg. commercial, etc (String),
                    "Copay": [
                                {
                                    "copayment": {"amount": String, "currency": String},
                                    "service_type_codes": ["UC", "33", "48", "50", "86", "98"],
                                    "coverage_level": "individual",
                                    "service_types": ["urgent_care", "chiropractic", "hospital_inpatient", "hospital_outpatient",
                                    "emergency_services", "professional_physician_visit_office"],
                                    "in_plan_network": "not_applicable"
                                }
                             ],
                    "Consumer Group Number": String,
                    "Service Types": [
                                        "health_benefit_plan_coverage",
                                        "vision_optometry",
                                        "mental_health",
                                        "urgent_care",
                                        "medical_care",
                                        "chiropractic",
                                        "hospital",
                                        "hospital_inpatient",
                                        "hospital_outpatient",
                                        "emergency_services",
                                        "professional_physician_visit_office
                                     ],
                    "Coinsurance Benefits": [
                                                {
                                                    "coverage_level": "individual",
                                                    "service_type_codes": ["33"],
                                                    "benefit_percent": 0.2,
                                                    "service_types": ["chiropractic"],
                                                    "in_plan_network": "not_applicable"
                                                },
                                                {
                                                    "coverage_level": "individual",
                                                    "service_type_codes": ["50", "48", "98", "86", "UC"],
                                                    "benefit_percent": 0.2,
                                                    "service_types": ["hospital_outpatient", "hospital_inpatient", "professional_physician_visit_office", "emergency_services", "urgent_care"],
                                                    "in_plan_network": "yes"
                                                },
                                                {
                                                    "coverage_level": "individual",
                                                    "service_type_codes": ["48", "98", "86", "UC", "50"],
                                                    "benefit_percent": 0.4,
                                                    "service_types": ["hospital_inpatient", "professional_physician_visit_office", "emergency_services", "urgent_care", "hospital_outpatient"],
                                                    "in_plan_network": "no"
                                                }
                                            ],
                    "Plan Description": eg. "CHOICE PLUS" (String),
                    "Plan is Active": Boolean,
                    "Deductibles": {
                                        "Calendar Year Amounts": [
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "not_applicable",
                                                                        "coverage_level": "family",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "no",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "yes",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["chiropractic"],
                                                                        "in_plan_network": "no",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["33"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    }
                                                                ]
                                    },
                    "Out of Pocket": {
                                        "Calendar Year Amounts": [
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "yes",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "no",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    }
                                                                ]
                                    }
                }
    }
    ```

- If consumer eligibility data is found and parsed with no errors,
    - "Error Code" will be 0
    - Dictionary corresponding to the "Data" key will have values for all the above keys in that format.
- If there was an error retrieving or parsing consumer eligibility data,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error retrieving or parsing consumer eligibility data.
    - Dictionary corresponding to the "Data" key may have keys ommitted or values of None.