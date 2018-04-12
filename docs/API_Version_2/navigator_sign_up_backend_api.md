## Navigator Sign Up Backend API README

### Navigator Sign Up Backend API
To create rows in the Navigators table in the database from the navigator sign up page on the Care Advisors site, make a PUT request to: http://picbackend.herokuapp.com/v2/navigator_sign_up/. 

- The headers of the request should include: 
    - "Content-Type: "application/json""
    - "X-Requested-With: 'XMLHttpRequest'"
    
The body of the request should be a JSON document using the following template:

```
{
    "first_name": String,
    "last_name": String,
    "email": String,

    'add_healthcare_locations_worked': [
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
    
    'add_insurance_carrier_specialties': [
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
                "degree_type": String ("masters", "bachelors", "high school", or "associate")
            }(All keys must be present when creating an education row),
            ...
        ],
        "create_job_rows": [
            {
                "title": String,
                "company": String,
                "description": String
            }(All keys must be present when creating an job row),
        ],
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
    - To create a row in the Navigators table from the navigator sign up page, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - 'add_healthcare_locations_worked'
            - 'add_healthcare_service_expertises'
            - 'add_insurance_carrier_specialties'
            - create_resume_row
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"]
            - create_resume_row["create_education_rows"][index]["start_year_datetime"]
            - create_resume_row["create_education_rows"][index]["end_year_datetime"]
            - create_resume_row["create_job_rows"]
            - create_resume_row["create_job_rows"][index]["start_year_datetime"]
            - create_resume_row["create_job_rows"][index]["end_year_datetime"]
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
            - 'add_healthcare_locations_worked'[index]['name']
            - 'add_healthcare_locations_worked'[index]['state_province']
            - 'add_healthcare_service_expertises'[index]
            - 'remove_healthcare_service_expertises'[index]
            - 'add_insurance_carrier_specialties'[index]['name']
            - 'add_insurance_carrier_specialties'[index]['state_province']
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"][index]["school"]
            - create_resume_row["create_education_rows"][index]["major"]
            - create_resume_row["create_education_rows"][index]["degree_type"]
            - create_resume_row["create_job_rows"][index]["description"]
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
        
        - Keys that can be Null
            - 'add_healthcare_locations_worked'[index]['name']
            - 'add_healthcare_locations_worked'[index]['state_province']
            - 'add_insurance_carrier_specialties'[index]['name']
            - 'add_insurance_carrier_specialties'[index]['state_province']
            - create_resume_row["profile_description"]
            - create_resume_row["create_education_rows"][index]["school"]
            - create_resume_row["create_education_rows"][index]["major"]
            - create_resume_row["create_education_rows"][index]["degree_type"]
            - create_resume_row["create_education_rows"][index]["start_year_datetime"]
            - create_resume_row["create_education_rows"][index]["end_year_datetime"]
            - create_resume_row["create_job_rows"][index]["description"]
            - create_resume_row["create_job_rows"][index]["start_year_datetime"]
            - create_resume_row["create_job_rows"][index]["end_year_datetime"]
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
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.

### Navigator Sign Up Picture Edit Page
- To view/change the profile picture for a given Navigators table row, make a GET request to http://picbackend.herokuapp.com/v2/navigator_pic/ with the following Mandatory parameters: "id",

### Navigator Resume File Edit Page
- To view/change the resume_file column for a given Navigators table row, make a GET request to http://picbackend.herokuapp.com/v2/nav_resume/ with the following Mandatory parameters: "id",
