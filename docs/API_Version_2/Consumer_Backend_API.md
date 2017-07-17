## Consumer Account Backend API

### Consumer Data Submission API
To modify or add members of the PICConsumer class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/consumers/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"First Name": String,
"Middle Name": String,
"Last Name": String,
"Email": String,
"Phone Number": String,
"Met Navigator At": String,
"Household Size": Integer,
"Navigator Notes": [
                        "These are",
                        "sample notes",
                        "navigators write about consumers",
                        ...
                    ],
"Plan": String,
"Preferred Language": String,
"Navigator Database ID": Integer,

Address Keys(Every field within address can be given as an empty string. Address will only be recorded/updated iff a full address is given)
"Address Line 1": String,
"Address Line 2": String,
"City": String,
"State": String,
"Zipcode": String,

"date_met_nav":{"Day": Integer,
                "Month": Integer,
                "Year": Integer},
                                
"cps_consumer": Boolean (Whether or not this consumer is a CPS consumer),
"cps_info": {
                "primary_dependent": {
                                        "first_name": String (Required when "Consumer Database ID" is omitted),
                                        "last_name": String (Required when "Consumer Database ID" is omitted),
                                        "Consumer Database ID": Integer (Required when "first_name" and "last_name" are omitted)
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
                                                "Consumer Database ID": Integer (Required when "first_name" and "last_name" are omitted)
                                                "force_create_consumer": Boolean (Set to True to create new Consumer instance despite possible matches in db),
                                             },
                                             ...
                                        ],
                "app_type": String (Must be one of these choices: "Medicaid", "SNAP", "Medicaid/SNAP", "Redetermination", "Plan Selection", "Fax FCRC", "Education", "MMCO", "Not Available"),
                "app_status": String (Must be one of these choices: "Submitted", "Pending", "Approved", "Denied", "Not Available"),
                "point_of_origin": String (Must be one of these choices: "Walk-in", "Appointment", "Referral from call", "Referral from school letter", "Enrollment event", "Not Available"),
            }(Contains relevant CPS info),

"Consumer Database ID": Integer,
"Database Action": String,
"create_backup": Boolean (Whether or not to create a backup instance of this consumer),
"force_create_consumer": Boolean (Set to True to create new Consumer instance despite possible matches in db),
}
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

- Adding a consumer database entry.
    - To add a consumer database entry, the value for "Database Action" in the JSON Body must equal "Consumer Addition".
    
        - Keys that can be omitted:
            - "create_backup"
            - "force_create_consumer"
            - "cps_consumer"(Must be present and True if "cps_info" is present.)
            - "cps_info" (Must be present if "cps_consumer" is True.)
            - cps_info["primary_dependent"]["first_name"]
            - cps_info["primary_dependent"]["last_name"]
            - cps_info["primary_dependent"]["Consumer Database ID"]
            - cps_info["primary_dependent"]["force_create_consumer"]
            - cps_info["secondary_dependents"]
            - cps_info["secondary_dependents"][index]["first_name"]
            - cps_info["secondary_dependents"][index]["last_name"]
            - cps_info["secondary_dependents"][index]["Consumer Database ID"]
            - cps_info["secondary_dependents"][index]["force_create_consumer"]
            - "Consumer Database ID"
            
        - Keys that can be empty strings:
            - "Middle Name"
            - "Email"
            - "Phone Number"
            - "Plan"
            - "Preferred Language"
            - "Address Line 1"
            - "Address Line 2"
            - "City"
            - "State"
            - "Zipcode"
        
        - Keys that can be empty arrays
            - "Navigator Notes"
            - cps_info["secondary_dependents"]
        
        - Keys that can be Null
            - "date_met_nav"
        
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Modifying a consumer database entry.
    - To modify a consumer database entry, the value for "Database Action" in the JSON Body must equal "Consumer Modification".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "Consumer Database ID"
    - Note: at least one key other than "Consumer Database ID" and "Database Action" must be present
    
        - Keys that can be omitted:
            - all except "Consumer Database ID" and "Database Action"
        
        - Keys that can be empty strings:
            - "Middle Name"
            - "Email"
            - "Phone Number"
            - "Plan"
            - "Preferred Language"
            - "Address Line 1"
            - "Address Line 2"
            - "City"
            - "State"
            - "Zipcode"
         
         - Keys that can be empty arrays
            - "Navigator Notes"
            - cps_info["secondary_dependents"]
        
        - Keys that can be Null
            - "date_met_nav"
            - "cps_info"
        
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the updated entry

- Deleting a consumer database entry.
    - To delete a consumer database entry, the value for "Database Action" in the JSON Body must equal "Consumer Deletion".
    
        - Keys that can be omitted:
            - all except "Consumer Database ID" and "Database Action"
        
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
### Consumer Data Retrieval API
- To retrieve consumer data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/consumers/ with the following parameters(at least one required)
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    - A maximum of 20 consumer records with full fields will be returned due to size constraints
        - The rest are consumer database IDs
        - Links to pages with the rest of the full records for your query will be given if you request without "page" parameter
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "fname" corresponds to consumer first name.
            - Can be multiple values separated by commas.
        - "lname" corresponds to consumer last name.
            - Can be multiple values separated by commas.
            - "fname" and "lname" can be given simultaneously as parameters. If so, only one value each is permitted.
        - "email" corresponds to consumer email.
            - Can be multiple values separated by commas.
        - "region" corresponds to consumer region.
            - Can be multiple values separated by commas.
        - "id" corresponds to consumer class database id.
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all consumer enteties
            
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - "navid" corresponds to staff member class database id.
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
                "Email": String,
                "Phone Number": String,
                "Database ID": Integer,
                "Preferred Language": String,
                "First Name": String,
                "Middle Name": String,
                "Last Name": String,
                "date_met_nav": String (Can be Null),
                "Navigator": String,
                "Navigator Notes": [
                                        "These are",
                                        "sample notes",
                                        "navigators write about consumers",
                                        ...
                                    ],
                "Met Navigator At": String,
                "Household Size": Integer,
                "Plan": String,
                "Best Contact Time": String,
                "address": Will either be None or a dictionary of the following form:
                           {
                            "Address Line 1": String,
                            "Address Line 2": String,
                            "City": String,
                            "State": String,
                            "Zipcode": String,
                            "Country": String,
                           },
                           
                "cps_consumer": Boolean,
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
            up to 20 full record consumer entries,
            2(Database IDs for the rest),
            6,
            9
        ],
        "Status": {
            "Version": 2.0,
            "Error Code": Integer,
            "Warnings": Array,
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
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
- If "page" parameter is missing and there is more than one page of customer instances to display with all fields, "Page
    URLs" key will be present in the root response dictionary.
    
    
### Consumer Backup Data Retrieval API
- To retrieve backup consumer data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/backup_consumers/ with the following parameters(at least one required)
    - A maximum of 20 consumer records with full fields will be returned due to size constraints
        - The rest are consumer database IDs
        - Links to pages with the rest of the full records for your query will be given if you request without "page" parameter
    - "fname" corresponds to consumer first name.
    - "lname" corresponds to consumer last name.
        - "fname" and "lname" can be given simultaneously as parameters. If so, only one value each is permitted.
    - "email" corresponds to consumer email.
    - "region" corresponds to consumer region.
    - "id" corresponds to consumer class database id.
        - passing "all" as the value will return all consumer enteties
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
                "date_met_nav": String (Can be Null),
                "Navigator": String,
                "Navigator Notes": [
                                        "These are",
                                        "sample notes",
                                        "navigators write about consumers",
                                        ...
                                    ],
                "Met Navigator At": String,
                "Household Size": Integer,
                "Plan": String,
                "Best Contact Time": String,
                "address": Will either be None or a dictionary of the following form:
                           {
                            "Address Line 1": String,
                            "Address Line 2": String,
                            "City": String,
                            "State": String,
                            "Zipcode": String,
                            "Country": String,
                           },
                           
                "cps_consumer": Boolean,
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
            up to 20 full record consumer entries,
            2(Database IDs for the rest),
            6,
            9
        ],
        "Status": {
            "Version": 2.0,
            "Error Code": Integer,
            "Warnings": Array,
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
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
- If "page" parameter is missing and there is more than one page of customer instances to display with all fields, "Page
    URLs" key will be present in the root response dictionary.