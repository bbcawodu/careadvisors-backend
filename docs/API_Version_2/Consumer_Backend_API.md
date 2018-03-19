## Consumer Account Backend API

### Consumer Data Submission API
To create, update, or delete rows in the PICConsumer table in the database, make a PUT request to: http://picbackend.herokuapp.com/v2/consumers/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
    "first_name": String,
    "middle_name": String,
    "last_name": String,
    "email": String,
    "phone": String,
    "met_bav_at": String,
    "household_size": Integer,
    "consumer_notes": [
        "These are",
        "sample notes",
        "navigators write about consumers",
        ...
    ],
    "plan": String,
    "preferred_language": String,
    "best_contact_time": String,
    "navigator_id": Integer,
    
    Address Keys(Every field within address can be given as an empty string. Address will only be recorded/updated iff a full address is given)
    "address_line_1": String,
    "address_line_2": String,
    "city": String,
    "state_province": String(2 letter code),
    "zipcode": String,
    
    "date_met_nav":{
        "Day": Integer,
        "Month": Integer,
        "Year": Integer
    },
    
    "create_case_management_rows": [
        {
            "management_step": Integer,
            "management_notes": String,
        },
        ...
    ],
    "update_case_management_rows": [
        {
            "management_step": Integer,
            "management_notes": String,
            "id": Integer
        },
        ...
    ],
    "delete_case_management_rows": [
        Integer,
        Integer,
        Integer
        ...
    ],
    
    'billing_amount': Float,
    'consumer_need': String,
    'service_expertise_need': String,
    'insurance_carrier': {
        'name': String,
        'state_province': String(2 letter code),
    },
    'add_healthcare_locations_used': [
        String,
        ...
    ],
    'remove_healthcare_locations_used': [
        String,
        ...
    ],
                    
    "cps_info": {
                    "primary_dependent": {
                                            "first_name": String (Required when "Consumer Database ID" is omitted),
                                            "last_name": String (Required when "Consumer Database ID" is omitted),
                                            "Consumer Database ID": Integer (Required when "first_name" and "last_name" are omitted),
                                            "force_create_consumer": Boolean (Set to True to create new Consumer instance despite possible matches in db),
                                         },
                    "cps_location": String (Must be the name of a NavMetricsLocation instance with cps_location=True),
                    "apt_date": {
                                    "Day": Integer,
                                    "Month": Integer,
                                    "Year": Integer,
                              },
                    "target_list": Boolean,
                    "phone_apt": Boolean,
                    "case_mgmt_type": String,
                    "case_mgmt_status": String (Must be one of these choices: "Open", "Resolved", "Not Available"),
                    "secondary_dependents": [
                                                 {
                                                    "first_name": String (Required when "Consumer Database ID" is omitted),
                                                    "last_name": String (Required when "Consumer Database ID" is omitted),
                                                    "Consumer Database ID": Integer (Required when "first_name" and "last_name" are omitted),
                                                    "force_create_consumer": Boolean (Set to True to create new Consumer instance despite possible matches in db),
                                                 },
                                                 ...
                                            ],
                    "app_type": String (Must be one of these choices: "Medicaid", "SNAP", "Medicaid/SNAP", "Redetermination", "Plan Selection", "Fax FCRC", "Education", "MMCO", "Not Available"),
                    "app_status": String (Must be one of these choices: "Submitted", "Pending", "Approved", "Denied", "Not Available"),
                    "point_of_origin": String (Must be one of these choices: "Walk-in", "Appointment", "Referral from call", "Referral from school letter", "Enrollment event", "Not Available"),
                }(Contains relevant CPS info),
    
    "id": Integer,
    "db_action": String,
    "create_backup": Boolean (Whether or not to create a backup instance of this consumer),
    "force_create_consumer": Boolean (Set to True to create new Consumer instance despite possible matches in db),
}
```


The Following is a list of possible consumer_need values with corresponding model constant names:
```
[
    CHOOSE_A_DOC = "choose a doctor",
    BILLING_ISSUES = "billing issues",
    N_A = "Not Available"
]
```


In response, a JSON document will be displayed with the following format:
```
{
    "Status": {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array,
            "Warnings": Array,
           },
    "Data": Dictionary Object or "Deleted",
}
```

- Create a PICConsumer database row.
    - To create a row in the PICConsumer table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "best_contact_time"
            - "create_backup"
            - "force_create_consumer"
            - "cps_info"
            - cps_info["primary_dependent"]["first_name"]
            - cps_info["primary_dependent"]["last_name"]
            - cps_info["primary_dependent"]["Consumer Database ID"]
            - cps_info["primary_dependent"]["force_create_consumer"]
            - cps_info["secondary_dependents"]
            - cps_info["secondary_dependents"][index]["first_name"]
            - cps_info["secondary_dependents"][index]["last_name"]
            - cps_info["secondary_dependents"][index]["Consumer Database ID"]
            - cps_info["secondary_dependents"][index]["force_create_consumer"]
            - "id"
            - "create_case_management_rows"
            - 'billing_amount'
            - 'consumer_need'
            - 'service_expertise_need'
            - insurance_carrier['name']
            - insurance_carrier['state_province']
            - 'add_healthcare_networks_used'
            - 'remove_healthcare_locations_used'
            
        - Keys that can be empty strings:
            - "middle_name"
            - "best_contact_time"
            - "email"
            - "phone"
            - "plan"
            - "preferred_language"
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - 'consumer_need'
            - 'service_expertise_need'
        
        - Keys that can be empty arrays
            - "consumer_notes"
            - cps_info["secondary_dependents"]
        
        - Keys that can be Null
            - "date_met_nav"
            - "cps_info"
            - insurance_carrier
            
        - Keys that WILL NOT be read
            - "update_case_management_rows"
            - "delete_case_management_rows"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a PICConsumer database row.
    - To update a row in the PICConsumer table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - "middle_name"
            - "best_contact_time"
            - "email"
            - "phone"
            - "plan"
            - "preferred_language"
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - 'consumer_need'
            - 'service_expertise_need'
         
         - Keys that can be empty arrays
            - "consumer_notes"
            - cps_info["secondary_dependents"]
        
        - Keys that can be Null
            - "date_met_nav"
            - "cps_info"
            - insurance_carrier
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a PICConsumer database row.
    - To delete a row in the PICConsumer table, the value for "db_action" in the JSON Body must equal "delete".
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is "Deleted".
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
### Consumer Data Retrieval API
- To retrieve consumer data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/consumers/ with the following parameters(at least one required)
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    - A maximum of 20 consumer record objects with all of the keys will be returned in order to limit the size of the response BODY.
        - The rest of the record objects will only have one key: "Database ID"
        - If the request does not include the "page" parameter:
            - "Page URLs" will be a key in the root of the JSON response Body.
                - The value of this key is an array of strings. Each string is a url for more full consumer records for the inital request.
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "first_name" corresponds to consumer first name.
            - Can be multiple values separated by commas.
        - "last_name" corresponds to consumer last name.
            - Can be multiple values separated by commas.
            - "first_name" and "last_name" can be given simultaneously as parameters. If so, only one value each is permitted.
        - "email" corresponds to consumer email.
            - Can be multiple values separated by commas.
        - "region" corresponds to consumer region.
            - Can be multiple values separated by commas.
        - "id" corresponds to consumer class database id.
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all consumer enteties
            
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - "nav_id" corresponds to staff member class database id.
            - Can be multiple values separated by commas.
        - "is_cps_consumer" corresponds to whether consumer is a Chicago Public Schools consumer.
            - must be of type boolean (true or false)
        - "page" corresponds to the current page of consumer instances to be displayed with full fields.
            - if this parameter is missing, the first 20 consumer instances will be displayed with full fields.
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "email": String,
                "phone": String,
                "id": Integer,
                "preferred_language": String,
                "first_name": String,
                "middle_name": String,
                "last_name": String,
                "date_met_nav": String (Can be Null),
                "navigator": String,
                "consumer_notes": [
                    "These are",
                    "sample notes",
                    "navigators write about consumers",
                    ...
                ],
                "case_management_rows": [
                    {
                        "management_step": 2,
                        "management_notes": "askjnksanfksaf"
                    },
                    {
                        "management_step": 5,
                        "management_notes": "askjnsagfksaf"
                    },
                    ...
                ],
                "met_nav_at": String,
                "household_size": Integer,
                "plan": String,
                "best_contact_time": String,
                'billing_amount': Float,
                'consumer_need': String,
                'service_expertise_need': String,
                'insurance_carrier': {
                    'name': String,
                    'state_province': String(2 letter code),
                },
                'add_healthcare_networks_used': [
                    String,
                    ...
                ],
                'remove_healthcare_networks_used': [
                    String,
                    ...
                ],
                "address": Will either be None or a dictionary of the following form:
                           {
                            "address_line_1": String,
                            "address_ine_2": String,
                            "city": String,
                            "state_province": String,
                            "zipcode": String,
                            "country": String,
                           },
                           
                "cps_info": {
                                "primary_dependent": {
                                                        "first_name": String,
                                                        "last_name": String,
                                                     },
                                "cps_location": String,
                                "apt_date"{
                                                "Day": Integer,
                                                "Month": Integer,
                                                "Year": Integer,
                                          },
                                "target_list": Boolean,
                                "phone_apt": Boolean,
                                "case_mgmt_type": String,
                                "case_mgmt_status": String,
                                "secondary_dependents": [
                                                             {
                                                                "first_name": String,
                                                                "last_name": String,
                                                             },
                                                             ...
                                                        ],
                                "app_type": String,
                                "app_status": String,
                            },
            },
            ...,
            ...,
            ...,
            up to 20 full record consumer record objects,
            {"Database ID": 2}(Incomplete consumer record with "Database ID" as its only key),
            {"Database ID": 6}(Incomplete consumer record with "Database ID" as its only key),
            {"Database ID": 9}(Incomplete consumer record with "Database ID" as its only key)
        ],
        "Status": {
            "Version": 2.0,
            "Error Code": Integer,
            "Warnings": Array,
            "Errors": Array
        },
        "Page URLs": Array of strings (Will be missing if "page" parameter is in request query string OR there are less than 20 consumer record objects in the array for the "Data" key.)
    }
    ```

- If consumers are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If consumers are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
- If "page" parameter is missing and there is more than one page of customer instances to display with all fields, "Page
    URLs" key will be present in the root response dictionary.
    
    
### Consumer Backup Data Retrieval API
- To retrieve backup consumer data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/backup_consumers/ with the following parameters(at least one required)
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    - A maximum of 20 consumer record objects with all of the keys will be returned in order to limit the size of the response BODY.
        - The rest of the record objects will only have one key: "Database ID"
        - If the request does not include the "page" parameter:
            - "Page URLs" will be a key in the root of the JSON response Body.
                - The value of this key is an array of strings. Each string is a url for more full consumer records for the inital request.
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "first_name" corresponds to consumer first name.
            - Can be multiple values separated by commas.
        - "last_name" corresponds to consumer last name.
            - Can be multiple values separated by commas.
            - "first_name" and "last_name" can be given simultaneously as parameters. If so, only one value each is permitted.
        - "email" corresponds to consumer email.
            - Can be multiple values separated by commas.
        - "region" corresponds to consumer region.
            - Can be multiple values separated by commas.
        - "id" corresponds to consumer class database id.
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all consumer enteties
            
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - "nav_id" corresponds to staff member class database id.
            - Can be multiple values separated by commas.
        - "is_cps_consumer" corresponds to whether consumer is a Chicago Public Schools consumer.
            - must be of type boolean (true or false)
        - "page" corresponds to the current page of consumer instances to be displayed with full fields.
            - if this parameter is missing, the first 20 consumer instances will be displayed with full fields.
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "email": String,
                "phone": String,
                "id": Integer,
                "preferred_language": String,
                "first_name": String,
                "middle_name": String,
                "last_name": String,
                "date_met_nav": String (Can be Null),
                "navigator": String,
                "consumer_notes": [
                    "These are",
                    "sample notes",
                    "navigators write about consumers",
                    ...
                ],
                "case_management_rows": [
                    {
                        "management_step": 2,
                        "management_notes": "askjnksanfksaf"
                    },
                    {
                        "management_step": 5,
                        "management_notes": "askjnsagfksaf"
                    },
                    ...
                ],
                "met_nav_at": String,
                "household_size": Integer,
                "plan": String,
                "best_contact_time": String,
                "address": Will either be None or a dictionary of the following form:
                           {
                            "address_line_1": String,
                            "address_ine_2": String,
                            "city": String,
                            "state_province": String,
                            "zipcode": String,
                            "country": String,
                           },
                           
                "cps_info": {
                                "primary_dependent": {
                                                        "first_name": String,
                                                        "last_name": String,
                                                     },
                                "cps_location": String,
                                "apt_date"{
                                                "Day": Integer,
                                                "Month": Integer,
                                                "Year": Integer,
                                          },
                                "target_list": Boolean,
                                "phone_apt": Boolean,
                                "case_mgmt_type": String,
                                "case_mgmt_status": String,
                                "secondary_dependents": [
                                                             {
                                                                "first_name": String,
                                                                "last_name": String,
                                                             },
                                                             ...
                                                        ],
                                "app_type": String,
                                "app_status": String,
                            },
            },
            ...,
            ...,
            ...,
            up to 20 full record consumer record objects,
            {"Database ID": 2}(Incomplete consumer record with "Database ID" as its only key),
            {"Database ID": 6}(Incomplete consumer record with "Database ID" as its only key),
            {"Database ID": 9}(Incomplete consumer record with "Database ID" as its only key)
        ],
        "Status": {
            "Version": 2.0,
            "Error Code": Integer,
            "Warnings": Array,
            "Errors": Array
        },
        "Page URLs": Array of strings (Will be missing if "page" parameter is in request query string OR there are less than 20 consumer record objects in the array for the "Data" key.)
    }
    ```

- If consumers are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If consumers are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
- If "page" parameter is missing and there is more than one page of customer instances to display with all fields, "Page
    URLs" key will be present in the root response dictionary.