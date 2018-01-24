## CPS Staff Table Enpoints Documentation

#### staff table create, update, and delete endpoint.
To create, update, or delete rows of the CPSStaff table in the database, make a PUT request to: http://picbackend.herokuapp.com/cps/v1/staff/. 

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"first_name": String,
"last_name": String,
"email": String,
"user_type": String,
"county": String,
"base_locations": [Strings (Can be None or empty string)], # If any locations are not found, an error will be added and the staff row will still be saved
"id": Integer(Required when "Database Action" == "update" or "delete"),
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

- Create a row in the CPSStaff table.
    - To create a row in the CPSStaff table, the value for "db_action" in the POST request must equal "create".
        - Keys that can be omitted:
            - "id"
            
        - Keys that can be empty strings:
            - base_locations[index]
        
        - Keys that can be empty arrays
            - base_locations
        
        - Keys that can be Null
            - base_locations[index]        
    - The response BODY will be JSON formatted text with a dictionary object as the value for the "Data" key.
        - It contains the key "db_row", the value for which is an object containing the fields of the created row.
    
- Update a row in the CPSStaff Table.
    - To update a row in the CPSStaff table, the value for "db_action" in the POST request must equal "update".
        - Keys that can be omitted:
            - "first_name"
            - "last_name"
            - "email"
            - "user_type"
            - "county"
            - "base_locations"
            
        - Keys that can be empty strings:
            - base_locations[index]
        
        - Keys that can be empty arrays
            - base_locations
        
        - Keys that can be Null
            - base_locations[index]        
    - The response BODY will be JSON formatted text with a dictionary object as the value for the "Data" key.
        - It contains the key "db_row", the value for which is an object containing the fields of the updated row.

- Delete a row in the CPSStaff Table.
    - To delete a row in the CPSStaff table, the value for "db_action" in the POST request must equal "delete".
    - The only other field should be "id".
    - The response BODY will be JSON formatted text with a dictionary object as the value for the "Data" key.
        - It contains the key "db_row", the value for which is the string "Deleted".
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
#### Staff table read endpoint.
- To read rows from the CPSStaff table of the backend, submit a GET request to http://picbackend.herokuapp.com/cps/v1/staff/
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
                "base_locations": [{
                                    "Location Name": String,
                                    "Address Line 1": String,
                                    "Address Line 2": String,
                                    "City": String,
                                    "State": String,
                                    "Zipcode": String,
                                    "Country": String,
                                    "Database Action": String
                                 },
                                  ...(Can be Empty)],
                "consumers":[
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
  
- If rows are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If rows are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.


### Staff Picture Edit Page
- To view/change the profile picture for a given staff member, submit a GET request to http://picbackend.herokuapp.com/cps/v1/staff_pic/ with the following Mandatory parameters: "id",