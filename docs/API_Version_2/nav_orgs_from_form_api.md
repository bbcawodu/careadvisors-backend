## Navigator Organizations From Care Advisors Form Backend README

### Navigator Organizations From Form Edit API
To create, update, or delete rows in the NavOrgsFromOnlineForm table in the database, make a PUT request to: http://picbackend.herokuapp.com/v2/nav_orgs_from_form/. 

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
    "company_name": String,
    
    Address Keys(Every field within address can be given as an empty string. Address will only be recorded/updated iff a full address is given)
    "address_line_1": String,
    "address_line_2": String,
    "city": String,
    "state_province": String(2 letter code),
    "zipcode": String,
    
    "estimated_monthly_caseload": Integer(non-negative)
    "contact_first_name": String,
    "contact_last_name": String,
    "contact_email": String,
    "contact_phone": String,
    "appointment_datetime": String'(Must be a iso formatted date and time in UTC eg. 'YYYY-MM-DDTHH:MM:SS'),
    "appointment_datetime_2": String'(Must be a iso formatted date and time in UTC eg. 'YYYY-MM-DDTHH:MM:SS'),
    "appointment_datetime_3": String'(Must be a iso formatted date and time in UTC eg. 'YYYY-MM-DDTHH:MM:SS'),
            
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

- Create a NavOrgsFromOnlineForm database row.
    - To create a row in the NavOrgsFromOnlineForm table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "appointment_datetime_2"
            - "appointment_datetime_3"
            
        - Keys that can be empty strings:
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "estimated_monthly_caseload"
        
        - Keys that can be Null
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "appointment_datetime_2"
            - "appointment_datetime_3"
            - "estimated_monthly_caseload"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created entry
    
- Update a NavOrgsFromOnlineForm database row.
    - To update a row in the NavOrgsFromOnlineForm table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "estimated_monthly_caseload"
        
        - Keys that can be Null
            - "address_line_1"
            - "address_line_2"
            - "city"
            - "state_province"
            - "zipcode"
            - "appointment_datetime"
            - "appointment_datetime_2"
            - "appointment_datetime_3"
            - "estimated_monthly_caseload"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created entry

- Delete a NavOrgsFromOnlineForm database row.
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
    
### Navigator Organizations From Form Table Read API
- To read rows from the NavOrgsFromOnlineForm table of the backend db, make a GET request to http://picbackend.herokuapp.com/v2/nav_orgs_from_form/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "id" corresponds to database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all NavOrgsFromOnlineForm rows.
        - "email" corresponds to email.
            - Must be a string
            - Can be multiple values separated by commas.
        - "company_name" corresponds to the company_name column of the NavOrgsFromOnlineForm table.
            - Must be an ascii string that has all non-ascii characters url encoded
        - "phone_number" corresponds to the contact_phone column of the NavOrgsFromOnlineForm table.
            - Must be an integer
            - Must be in the following format: DDDDDDDDDD where D=base 10 digit
            - Can be multiple values separated by commas.
            
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - None
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "company_name": String,
                
                "address": {
                    "address_line_1": String,
                    "address_line_2": String,
                    "city": String,
                    "state_province": String(2 letter code),
                    "zipcode": String,
                }
                
                "estimated_monthly_caseload": Integer(non-negative)
                "contact_first_name": String,
                "contact_last_name": String,
                "contact_email": String,
                "contact_phone": String,
                "appointment_datetime": String',
                "appointment_datetime_2": String',
                "appointment_datetime_3": String',
                "id": Integer,
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
