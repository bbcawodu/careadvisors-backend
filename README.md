# Consumer Metrics and Appointments Backend

This is the code for the backend component of our metrics and appointments apps. It enables the API that transmits data between the frontend and the backend.



## Installation

This app runs on a django installation hosted on Heroku. To install Heroku for code editing, go to: https://devcenter.heroku.com/articles/getting-started-with-python#introduction and follow the instructions for your particular operating system.



## Presence Healthcare Appointment Scheduler Backend

### Presence Healthcare Appointment Addition API
To add an appointment to the database using our appointments API, make a POST request to: http://picbackend.herokuapp.com/submitappointment/. The POST data should be a JSON document which has the following format:

```
{
 "First Name": String,
 "Last Name": String,
 "Email": String,
 "Phone Number": String,
 "Preferred Language": String (Not Required),
 "Best Contact Time": String (Not Required),
 "Appointment": {
                 "Name": String,
                 "Street Address": String,
                 "City": String,
                 "State": String,
                 "Zip Code": String,
                 "Phone Number": String,
                 "Appointment Slot": {
                                      "Date": {
                                               "Month": Integer,
                                               "Day": Integer,
                                               "Year": Integer
                                              },
                                      "Start Time": {
                                                     "Hour": Integer,
                                                     "Minutes": Integer
                                                    },
                                      "End Time": {
                                                   "Hour": Integer,
                                                   "Minutes": Integer
                                                  }
                                     },
                 "Point of Contact": {
                                      "First Name": String,
                                      "Last Name": String,
                                      "Email": String,
                                      "Type": String
                                     }
                }
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
           }
}
```

- If there are no errors in the POSTed JSON doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "Status" dictionary.
    - An instance of the Appointment class corresponding to the POSTed JSON doc will be created and saved in the database.
        - If there isn't a consumer database entry with an email field corresponding to the POST, one is created.
        - If there isn't a location database entry with a name field corresponding to the POST, one is created.
        - If there isn't a staff database entry with an email field corresponding to the POST, one is created.
    
- If there are errors in the POSTed JSON doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        - Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.



### Presence Healthcare Appointments Viewer
Go to http://picbackend.herokuapp.com/viewappointments to view what appointments have been submitted by consumers and to whom they have been assigned.



## Staff Account Backend API

### Staff Data Submission API
To modify or add members of the PICStaff class in the database, submit a POST request to: http://picbackend.herokuapp.com/editstaff/. The POST data a JSON document using the following template:

```
{
"First Name": String,
"Last Name": String,
"Email": String,
"User Type": String,
"User County": String,
"Database ID": Integer(Required when "Database Action" == "Staff Modification" or "Staff Deletion"),
"Database Action": String,
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Adding a staff member database entry.
    - To add a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the added database entry.
    
- Modifying a staff member database entry.
    - To modify a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Modification".
    - All other fields must be filled.
    - All key value pairs in the POSTed JSON document correspond to updated fields for specified "Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the updated database entry.

- Deleting a staff member database entry.
    - To delete a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Staff Data Retrieval API
- To retrieve staff data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/staff? with the following optional parameters: "fname", "lname", "email", "id"
    - "fname" corresponds to first name.
    - "lname" corresponds to last name.
    - "email" corresponds to email.
    - "id" corresponds to database id.
        - passing "all" as the value will return all staff members
    - All parameters may have a single or multiple values separated by commas
    - One parameter is allowed at a time (only "fname" and "lname" can be grouped)
        - If "fname" and "lname" are given simultaneously as parameters, only one value each is permitted.
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Email": String,
                "Type": String,
                "Database ID": Integer,
                "County": String,
                "First Name": String,
                "Last Name": String,
                "Consumers":[
                                {
                                "First Name": String,
                                "Best Contact Time": String,
                                "Database ID": Integer,
                                "Last Name": String,
                                "Preferred Language": String,
                                "Navigator": String,
                                "Phone Number": String,
                                "Email": String
                                },
                                ....
                            ],
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- If staff members are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If staff members are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.



## Consumer Account Backend API

### Consumer Data Submission API
To modify or add members of the PICConsumer class in the database, submit a POST request to: http://picbackend.herokuapp.com/editconsumer/. The POST data a JSON document using the following template:

```
{
"First Name": String,
"Middle Name": String (Can be empty),
"Last Name": String,
"Email": String,
"Phone Number": String (Can be empty),
"Zipcode": String,
"Address": String (Can be empty),
"Met Navigator At": String,
"Household Size": Integer,
"Plan": String (Can be empty),
"Preferred Language": String (Can be empty),
"Navigator Database ID": Integer,
"Consumer Database ID": Integer(Required when "Database Action" == "Consumer Modification" or "Consumer Deletion"),
"Database Action": String,
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Adding a consumer database entry.
    - To add a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Addition".
    - All other fields except "Consumer Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the added database entry.
    
- Modifying a consumer database entry.
    - To modify a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Modification".
    - All other fields must be filled.
    - All key value pairs in the POSTed JSON document correspond to updated fields for specified "Consumer Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the updated database entry.

- Deleting a consumer database entry.
    - To delete a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Deletion".
    - The only other field should be "Consumer Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Consumer Data Retrieval API
- To retrieve consumer data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/consumers? with the following parameters(at least one required)
    - A maximum of 20 consumer records with full fields will be returned due to size constraints
        - The rest are consumer database IDs
        - Links to pages with the rest of the full records for your query will be given if you request without "page" parameter
    - "fname" corresponds to consumer first name.
    - "lname" corresponds to consumer last name.
        - "fname" and "lname" can be given simultaneously as parameters. If so, only one value each is permitted.
    - "email" corresponds to consumer email.
    - "id" corresponds to consumer class database id.
        - passing "all" as the value will return all staff members
    - "navid" corresponds to staff member class database id. (Can be combined with any of the above parameters)
    - "page" corresponds to the current page of consumer instances to be displayed with full fields. 
        - if this parameter is missing, the first 20 consumer instances will be displayed with full fields.
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Email": String,
                "Phone Number": String,
                "Database ID": Integer,
                "Preferred Language": String,
                "First Name": String,
                "Middle Name": String,
                "Last Name": String,
                "Navigator": String,
                "Zipcode": String,
                "Address": String,
                "Met Navigator At": String,
                "Household Size": Integer,
                "Plan": String,
                "Best Contact Time": String,
            },
            ...,
            ...,
            ...,
            up to 20 full record consumer entries,
            2(Database IDs for the rest),
            6,
            9
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        },
        "Page URLs": Array of strings (Will be missing if "page" parameter is given OR less than 20 consumers in results)
    }
    ```

- If consumers are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If consumers are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.
- If "page" parameter is missing and there is more than one page of customer instances to display with all fields, "Page
    URLs" key will be present in the root response dictionary. 
    
    
    
## Consumer Metrics Backend API

### Consumer Metrics Submission API
To submit an entry of consumer metrics data corresponding to a specific staff member, make a POST request to: http://picbackend.herokuapp.com/submitmetrics/. The POST data should be a JSON document which has the following format:

```
{
"Email": String,
"User Type": "IPC" or "Navigator",
"Consumer Metrics": {"Metrics Date":{"Day": Integer,
                                    "Month": Integer,
                                    "Year": Integer,},
                    "County": String,
                    "Zipcode": String,
                    "Received Education": Integer,
                    "Applied Medicaid": Integer,
                    "Selected QHP": Integer,
                    "Referred Medicaid or CHIP": Integer,
                    "Filed Exemptions": Integer,
                    "Received Post-Enrollment Support": Integer,
                    "Trends": String (Not Required),
                    "Success Story": String,
                    "Hardship or Difficulty": String,
                    "Outreach and Stakeholder Activities": String (Not Required),
                    "Plan Stats": [
                                    {"Issuer Name": String,
                                    "Enrollments": Integer,
                                    "Premium Type": String,
                                    "Metal Level": String},
                                    {},
                                    ....
                                  ],
                    }
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
           }
}
```

- If there are no errors in the POSTed JSON doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "Status" dictionary.
    - An instance of the MetricsSubmission class corresponding to the POSTed JSON doc will be created and saved in the database.
        - Only one metrics submission is allowed per day.
    
- If there are errors in the POSTed JSON doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        - Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Consumer Metrics Retrieval API.
- To retrieve metrics data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/metrics? with the following optional parameters: "fname", "lname", "email", "id", "county", "time", "groupby"
    - "fname" corresponds to staff member first name.
    - "lname" corresponds to staff member last name.
    - "email" corresponds to staff member email.
    - "id" corresponds to staff member class database id.
        - passing "all" as the value will return all staff members
    - "navid" corresponds to staff member class database id.
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Metrics Data": [
                {
                "Date Created": String,
                "Appointments Complex Medicaid": Integer,
                "Referred SHOP": Integer,
                "Filed Exemptions": Integer,
                "Enrolled SHOP": Integer,
                "Appointments Held": Integer,
                "Hardship or Difficulty": String,
                "Appointments Post-Enrollment Assistance": Integer,
                "County": String,
                "Trends": String,
                "Appointments Complex Market": Integer,
                "Outreach and Stakeholder Activities": String,
                "Referred Medicaid or CHIP": Integer,
                "Applied Medicaid": Integer,
                "Staff Member ID": Integer,
                "Submission Date": String,
                "Received Education": Integer,
                "Received Post-Enrollment Support": Integer,
                "Appointments Over 3 Hours": Integer,
                "Confirmation Calls": Integer,
                "Appointments Over Hour": Integer,
                "Success Story": String,
                "Selected QHP": Integer,
                "Comments": String,
                "Appointments Scheduled": Integer
                },
                ...,
                ...,
                ...,
                ],
                "Staff Information": {
                "Database ID": Integer,
                "First Name": String,
                "County": String,
                "Type": String,
                "Last Name": String,
                "Email": String
                }
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- If metrics reports are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If metrics reports are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.



### Pokitdok Eligibility Retrieval API.
- To retrieve parsed eligibility data from pokitdok for a consumer, submit a POST request to http://picbackend.herokuapp.com/v1/eligibility The POST data a JSON document using the following template:

```
{
"Birth Date":"YYYY-MM-DD" (Can be None),
"First Name": String (Can be None),
"Last Name": String (Can be None),
"Trading Partner ID": Plan name code which can be retrieved from trading partner API (String),
"Consumer Plan ID": String (Can be None)
}
```

- The consumer parameters ("Trading Partner ID" is mandatory) need to match one of these search patterns:
    - ["First Name", "Last Name", "Birth Date"]
    - ["First Name", "Last Name", "Consumer Plan ID"]
    - ["First Name", "Last Name", "Consumer Plan ID", "Birth Date"]
    - ["Consumer Plan ID", "Birth Date"]
    - ["Last Name", "Consumer Plan ID", "Birth Date"]
    
    
- The response will be a JSON document with the following format:
    ```
    {
        "Status": {
                    "Version": Integer,
                    "Error Code": Integer,
                    "Errors": Array
                  }
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
    
    
    
## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license
