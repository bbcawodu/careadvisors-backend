## Care Advisor Customer Backend API


## care_advisor_customer Table Entity Relationship Diagram

![care_advisor_customer Table Entity Relationship Diagram](care_advisor_customer_table_erd.jpg)


### Care Advisor Customer: Create, Update, and Delete Methods Endpoint
To create, update, or delete rows in the care_advisor_customer table of the database, make a PUT request to: http://picbackend.herokuapp.com/v2/care_advisor_customer/

- The header of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be JSON formatted text using the following template:

```
"
{
"first_name": String,
"last_name": String,
"email": String (Must be in the following format: username@domanname.domain),
"company_name": String,
"phone_number": String (Must be in the following format: DDDDDDDDDD where D=base 10 digit),
"id": Integer,
"db_action": String,
}
"
```

In response, JSON formatted text with the following format will be returned:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array
            "Data": {
                        "id": Integer or "deleted"
                    },
           }
}
```

- Creating a row in the care_advisor_customer table.
    - To create a row in the care_advisor_customer table, the value for the "db_action" key in the root object must equal "create_row".
    - Request root object information
        - Keys that MUST be omitted:
            - "id"
        - Keys that CAN be omitted:
            - None
        - Keys that can be empty strings:
            - None
        - Keys that can be Null
            - None
    - The response JSON formatted text will have a object as the value for the "Data" key.
        - It contains the key "db_id", the value for which is the database id of the created entry
    
- Updating a row in the care_advisor_customer table.
    - To update a row in the care_advisor_customer table, the value for the "db_action" key in the root object must equal "update_row".
    - Request root object information
        - Keys that MUST be omitted:
            - None
        - Keys that CAN be omitted:
            - "first_name"
            - "last_name"
            - "email"
            - "company_name"
            - "phone_number"
        - Keys that can be empty strings:
            - None
        - Keys that can be Null
            - None
    - The response JSON formatted text will have a object as the value for the "Data" key.
        - It contains the key "db_id", the value for which is the database id of the updated entry

- Deleting a row in the care_advisor_customer table.
    - To delete a row in the care_advisor_customer table, the value for the "db_action" key in the root object must equal "delete_row".
    - Request root object information
        - Keys that MUST be omitted:
            - all except "id" and "db_action"
        - Keys that CAN be omitted:
            - None
        - Keys that can be empty strings:
            - None
        - Keys that can be Null
            - None
    - The response JSON document will have a "Deleted" as the value for the "Data" key.

- If there ARE NO errors parsing the request body:
    - The value for the "Errors" key in the response root object will an empty array
    - The value for the "Error Code" key in the response root object will be 0.    
- If there ARE errors parsing the request body:
    - The "Error Code" key in the root response object will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" object.
        - Each object in the array is a string corresponding to an error in parsing the request BODY.
    - No changes are made to the database.
    
### Care Advisor Customer: Read Method Endpoint
- To read/query rows in the care_advisor_customer table of the database, make a GET request to http://picbackend.herokuapp.com/v2/care_advisor_customer/
    - Results returned in the response body will be filtered by the parameters given in the query string of the request url.
    - The parameters given in the query string can be divided into 2 categories: "primary" and "secondary"
    
    - "primary" parameters - One and exactly one of these parameters are required in every request query string.
        - "first_name" corresponds to the first_name column of the care_advisor_customer table.
            - Must be a string
            - Can be multiple values separated by commas.
        - "last_name" corresponds to the last_name column of the care_advisor_customer table.
            - Must be a string
            - Can be multiple values separated by commas.
        - "email" corresponds to the email column of the care_advisor_customer table.
            - Must be a string
            - Can be multiple values separated by commas.
        - "company_name" corresponds to the company_name column of the care_advisor_customer table.
            - Must be an ascii string that has all non-ascii characters url encoded
        - "phone_number" corresponds to the column of the care_advisor_customer table.
            - Must be an integer
            - Must be in the following format: DDDDDDDDDD where D=base 10 digit
            - Can be multiple values separated by commas.
        - "id" corresponds to the id column of the care_advisor_customer table.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all staff members.
        - SPECIAL CASE: Only "first_name" and "last_name" can be given simultaneously as parameters in the query string.
            - When "first_name" and "last_name" are given at the same time, only one value of each permitted for each parameter.
            
    - "Secondary" parameters - Any number of these parameters can be added to a request query string.
        - None
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "first_name": String,
                "last_name": String,
                "email": String,
                "company_name": String,
                "phone_number": String,
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

- NOTES
    - If the 'primary' parameter given in the query string is not 'id', results will be grouped by the 'primary' parameter that is given with the request.
        -Eg: If "first_name" is the "primary" parameter the results will be grouped like the following
            
            ```
            "Data": [
                [Results for first_name parameter 2],
                [Results for first_name parameter 1],
                [Results for first_name parameter 3],
                ...,
            ] (Order is arbitrary)
            ```
  
- If there ARE NO errors parsing the request body and rows in the care_advisor_customer table of the database ARE found:
    - The value for the "Errors" key in the response root object will an empty array
    - The value for the "Error Code" key in the response root object will be 0. 
- If there ARE errors parsing the request body or rows in the care_advisor_customer table of the database ARE NOT found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
