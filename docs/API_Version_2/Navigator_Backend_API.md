## Navigator Data Backend API

### Navigator Data Submission API
To create, update, or delete rows in the Navigators table in the database, make a PUT request to: http://picbackend.herokuapp.com/v2/navigators/. 

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
    "first_name": String,
    "last_name": String,
    "email": String,
    "type": String,
    "county": String,
    "add_base_locations": [
        String (Can be empty string),
        ...
    ](Names of Locations),
    "remove_base_locations": [
        String (Can be empty string),
        ...
    ](Names of Locations),
    "mpn": String(Can be Null or empty string),

    'add_healthcare_locations_worked': [
        {
            'name': String,
            'state_province': String(2 letter code),
        }(Both keys must be present to retrieve row),
        ...
    ],
    'remove_healthcare_locations_worked': [
        {
            'name': String,
            'state_province': String(2 letter code),
        }(Both keys must be present to retrieve row),
        ...
    ],
    
    'add_healthcare_service_expertises': [
        String,
        ...
    ],
    'remove_healthcare_service_expertises': [
        String,
        ...
    ],
    
    'add_insurance_carrier_specialties': [
        {
            'name': String,
            'state_province': String(2 letter code),
        }(Both keys must be present to retrieve row),
        ...
    ],
    'remove_insurance_carrier_specialties': [
        {
            'name': String,
            'state_province': String(2 letter code),
        }(Both keys must be present to retrieve row),
        ...
    ],

    "create_resume_row": {
        "profile_description": String (key must be present when creating an education row),
        "create_education_rows": [
            {
                "school": String,
                "major": String,
                "degree_type": String ("masters" or "bachelors")
            }(All keys must be present when creating an education row),
            ...
        ],
        "create_job_rows": [
            {
                "title": String,
                "company": String,
                "description": String
            }(All keys must be present when creating an education row),
        ],
    },

    "update_resume_row": {
        "profile_description": "applesauce",
        "create_education_rows": [
            {
                "school": String,
                "major": String,
                "degree_type": String ("masters" or "bachelors")
            },
            ...
        ],
        "update_education_rows": [
            {
                "school": String,
                "major": String,
                "degree_type": String ("masters" or "bachelors"),
                "id": Integer
            }(id must be present when updating),
            ...
        ],
        "delete_education_rows": [
            {
                "id": Integer
            },
            ...
        ],

        "create_job_rows": [
            {
                "title": String,
                "company": String,
                "description": String
            },
            ...
        ],
        "update_job_rows": [
            {
                "title": String,
                "company": String,
                "description": String,
                "id": Integer
            }(id must be present when updating),
        ],
        "delete_job_rows": [
            {
                "id": Integer
            },
            ...
        ],
        "id": Integer (id must be present when updating),
    },

    "delete_resume_row": {
        "id": Integer,
    },

    Address Keys(Every field within address can be given as an empty string. Address will only be recorded/updated iff a full address is given)
    "address_line_1": String,
    "address_line_2": String,
    "city": String,
    "state_province": String(2 letter code),
    "zipcode": String,

    "phone": String,
    "reported_region": String,
    "video_link": String,
    "navigator_organization", String,
            
    "id": Integer,
    "db_action": String,
}
```

In response, a JSON document will be displayed with the following format:
```
{
    "Status": {
        "Error Code": Integer,
        "Version": 2.0,
        "Errors": Array
        "Data": Dictionary Object or "Deleted",
    }
}
```

- Create a Navigators database row.
    - To create a row in the Navigators table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            - "add_base_locations"
            - "remove_base_locations"
            - 'add_healthcare_locations_worked'
            - 'remove_healthcare_locations_worked'
            - 'add_healthcare_service_expertises'
            - 'remove_healthcare_service_expertises'
            - 'add_insurance_carrier_specialties'
            - 'remove_insurance_carrier_specialties'
            - create_resume_row
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"]
            - create_resume_row["create_job_rows"]
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "phone"
            - "reported_region"
            - "video_link"
            - "navigator_organization"
            
        - Keys that can be empty strings:
            - "add_base_locations"[index]
            - "remove_base_locations"[index]
            - "mpn"
            - 'add_healthcare_locations_worked'[index]['name']
            - 'add_healthcare_locations_worked'[index]['state_province']
            - 'remove_healthcare_locations_worked'[index]['name']
            - 'remove_healthcare_locations_worked'[index]['state_province']
            - 'add_healthcare_service_expertises'[index]
            - 'remove_healthcare_service_expertises'[index]
            - 'add_insurance_carrier_specialties'[index]['name']
            - 'add_insurance_carrier_specialties'[index]['state_province']
            - 'remove_insurance_carrier_specialties'[index]['name']
            - 'remove_insurance_carrier_specialties'[index]['state_province']
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"][index]["school"]
            - create_resume_row["create_education_rows"][index]["major"]
            - create_resume_row["create_education_rows"][index]["degree_type"]
            - create_resume_row["create_job_rows"][index]["title"]
            - create_resume_row["create_job_rows"][index]["company"]
            - create_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["profile_description"]
            - update_resume_row["create_education_rows"][index]["school"]
            - update_resume_row["create_education_rows"][index]["major"]
            - update_resume_row["create_education_rows"][index]["degree_type"]
            - update_resume_row["update_education_rows"][index]["school"]
            - update_resume_row["update_education_rows"][index]["major"]
            - update_resume_row["update_education_rows"][index]["degree_type"]
            - update_resume_row["create_job_rows"][index]["title"]
            - update_resume_row["create_job_rows"][index]["company"]
            - update_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["update_job_rows"][index]["title"]
            - update_resume_row["update_job_rows"][index]["company"]
            - update_resume_row["update_job_rows"][index]["description"]
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "phone"
            - "reported_region"
            - "video_link"
        
        - Keys that can be empty arrays
            - "add_base_locations"
            - 'add_healthcare_locations_worked'
            - 'add_healthcare_service_expertises'
            - 'add_insurance_carrier_specialties'
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"]
            - create_resume_row["create_job_rows"]
            - update_resume_row["create_education_rows"]
            - update_resume_row["create_job_rows"]
        
        - Keys that can be Null
            - "mpn"
            - 'add_healthcare_locations_worked'[index]['name']
            - 'add_healthcare_locations_worked'[index]['state_province']
            - 'remove_healthcare_locations_worked'[index]['name']
            - 'remove_healthcare_locations_worked'[index]['state_province']
            - 'add_insurance_carrier_specialties'[index]['name']
            - 'add_insurance_carrier_specialties'[index]['state_province']
            - 'remove_insurance_carrier_specialties'[index]['name']
            - 'remove_insurance_carrier_specialties'[index]['state_province']
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"][index]["school"]
            - create_resume_row["create_education_rows"][index]["major"]
            - create_resume_row["create_education_rows"][index]["degree_type"]
            - create_resume_row["create_job_rows"][index]["title"]
            - create_resume_row["create_job_rows"][index]["company"]
            - create_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["profile_description"]
            - update_resume_row["create_education_rows"][index]["school"]
            - update_resume_row["create_education_rows"][index]["major"]
            - update_resume_row["create_education_rows"][index]["degree_type"]
            - update_resume_row["update_education_rows"][index]["school"]
            - update_resume_row["update_education_rows"][index]["major"]
            - update_resume_row["update_education_rows"][index]["degree_type"]
            - update_resume_row["create_job_rows"][index]["title"]
            - update_resume_row["create_job_rows"][index]["company"]
            - update_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["update_job_rows"][index]["title"]
            - update_resume_row["update_job_rows"][index]["company"]
            - update_resume_row["update_job_rows"][index]["description"]
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "phone"
            - "reported_region"
            - "video_link"
            - "navigator_organization"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created entry
    
- Update a Navigators database row.
    - To update a row in the Navigators table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - "add_base_locations"[index]
            - "remove_base_locations"[index]
            - "mpn"
            - 'add_healthcare_locations_worked'[index]['name']
            - 'add_healthcare_locations_worked'[index]['state_province']
            - 'remove_healthcare_locations_worked'[index]['name']
            - 'remove_healthcare_locations_worked'[index]['state_province']
            - 'add_healthcare_service_expertises'[index]
            - 'remove_healthcare_service_expertises'[index]
            - 'add_insurance_carrier_specialties'[index]['name']
            - 'add_insurance_carrier_specialties'[index]['state_province']
            - 'remove_insurance_carrier_specialties'[index]['name']
            - 'remove_insurance_carrier_specialties'[index]['state_province']
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"][index]["school"]
            - create_resume_row["create_education_rows"][index]["major"]
            - create_resume_row["create_education_rows"][index]["degree_type"]
            - create_resume_row["create_job_rows"][index]["title"]
            - create_resume_row["create_job_rows"][index]["company"]
            - create_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["profile_description"]
            - update_resume_row["create_education_rows"][index]["school"]
            - update_resume_row["create_education_rows"][index]["major"]
            - update_resume_row["create_education_rows"][index]["degree_type"]
            - update_resume_row["update_education_rows"][index]["school"]
            - update_resume_row["update_education_rows"][index]["major"]
            - update_resume_row["update_education_rows"][index]["degree_type"]
            - update_resume_row["create_job_rows"][index]["title"]
            - update_resume_row["create_job_rows"][index]["company"]
            - update_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["update_job_rows"][index]["title"]
            - update_resume_row["update_job_rows"][index]["company"]
            - update_resume_row["update_job_rows"][index]["description"]
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "phone"
            - "reported_region"
            - "video_link"
         
         - Keys that can be empty arrays
            - "add_base_locations"
        
        - Keys that can be Null
            - "mpn"
            - 'add_healthcare_locations_worked'[index]['name']
            - 'add_healthcare_locations_worked'[index]['state_province']
            - 'remove_healthcare_locations_worked'[index]['name']
            - 'remove_healthcare_locations_worked'[index]['state_province']
            - 'add_insurance_carrier_specialties'[index]['name']
            - 'add_insurance_carrier_specialties'[index]['state_province']
            - 'remove_insurance_carrier_specialties'[index]['name']
            - 'remove_insurance_carrier_specialties'[index]['state_province']
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"][index]["school"]
            - create_resume_row["create_education_rows"][index]["major"]
            - create_resume_row["create_education_rows"][index]["degree_type"]
            - create_resume_row["create_job_rows"][index]["title"]
            - create_resume_row["create_job_rows"][index]["company"]
            - create_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["profile_description"]
            - update_resume_row["create_education_rows"][index]["school"]
            - update_resume_row["create_education_rows"][index]["major"]
            - update_resume_row["create_education_rows"][index]["degree_type"]
            - update_resume_row["update_education_rows"][index]["school"]
            - update_resume_row["update_education_rows"][index]["major"]
            - update_resume_row["update_education_rows"][index]["degree_type"]
            - update_resume_row["create_job_rows"][index]["title"]
            - update_resume_row["create_job_rows"][index]["company"]
            - update_resume_row["create_job_rows"][index]["description"]
            - update_resume_row["update_job_rows"][index]["title"]
            - update_resume_row["update_job_rows"][index]["company"]
            - update_resume_row["update_job_rows"][index]["description"]
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "phone"
            - "reported_region"
            - "video_link"
            - "navigator_organization"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created entry

- Delete a Navigators database row.
    - To delete a row in the Navigators table, the value for "db_action" in the JSON Body must equal "delete".
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
    - If there are no errors in the JSON Body document:
        - It contains the key "row", the value for which is "Deleted".
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
### Navigator Data Retrieval API
- To read rows from the navigators table of the backend database, make a GET request to http://picbackend.herokuapp.com/v2/navigators/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "first_name" corresponds to first name.
            - Must be a string
            - Can be multiple values separated by commas.
        - "last_name" corresponds to last name.
            - Must be a string
            - Can be multiple values separated by commas.
        - "email" corresponds to email.
            - Must be a string
            - Can be multiple values separated by commas.
        - "mpn" corresponds to mpn.
            - Must be a string
            - Can be multiple values separated by commas.
        - "county" corresponds to navigator county.
            - Must be a string
            - Can be multiple values separated by commas.
        - "region" corresponds to the staff's default region.
            - Must be a string
        - "id" corresponds to database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all staff members.
        - SPECIAL CASE: Only "first_name" and "last_name" can be given simultaneously as parameters.
            - When "first_name" and "last_name" are given at the same time, only one value of each permitted.
            
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - None
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "email": String,
                "type": String,
                "id": Integer,
                "county": String,
                "region": String,
                "first_name": String,
                "last_name": String,
                "authorized_credentials": Boolean,
                "picture": Link,
                "base_location": [
                    {
                        "Location Name": String,
                        "Address Line 1": String,
                        "Address Line 2": String,
                        "City": String,
                        "State": String,
                        "Zipcode": String,
                        "Country": String,
                        "Database Action": String
                    },
                    ...(Can be Empty)
                ](Can be Empty),
                "mpn": String,
                "consumers":[
                    Integer,
                    ....
                ](Can be Empty),
                'healthcare_locations_worked': [
                    {
                        'name': String,
                        'state_province': String(2 letter code),
                    },
                    ...
                ](Can be empty),
                'healthcare_service_expertises': [
                    String,
                    ...
                ](Can be empty),
                'insurance_carrier_specialties': [
                    {
                        'name': String,
                        'state_province': String(2 letter code),
                    },
                    ...
                ](Can be empty),
                "resume_info": [
                    {
                        "profile_description": String,
                        "education_info": [
                            {
                                "school": String,
                                "major": String,
                                "degree_type": String
                            },
                            ...
                        ],
                        "job_info": [
                            {
                                "title": String,
                                "company": String,
                                "description": String
                            },
                            ...
                        ],
                    },
                    ...
                ](Can be empty),
                
                "address": {
                    "address_line_1": String,
                    "address_line_2": String,
                    "city": String,
                    "state_province": String(2 letter code),
                    "zipcode": String,
                },
            
                "phone": String,
                "reported_region": String,
                "video_link": String,
                "navigator_organization", String,
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": 2.0,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- NOTES: Results will be grouped by the "Primary" parameter that is given with the request.
    -Eg: If "first_name" is the "Primary" parameter the results will be grouped like the following
        
        ```
        "Data": [
            [Results for first_name parameter 2],
            [Results for first_name parameter 1],
            [Results for first_name parameter 3],
            ...,
        ] (Order is arbitrary)
        ```
  
- If staff members are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If staff members are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.


### Navigator Picture Edit Page
- To view/change the profile picture for a given Navigators table row, make a GET request to http://picbackend.herokuapp.com/v2/navigator_pic/ with the following Mandatory parameters: "id",