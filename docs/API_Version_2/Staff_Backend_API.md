## Staff Account Backend API

### Staff Data Submission API
To create, update, or delete rows in the PICStaff table in the database, make a PUT request to: http://picbackend.herokuapp.com/v2/staff/. 

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"First Name": String,
"Last Name": String,
"Email": String,
"User Type": String,
"User County": String,
"Base Location Names": [Strings (Can be Null or empty string)], # If any locations are not found, an error will be added and the staff member will still be saved
"MPN": String(Can be Null or empty string),
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

- Create a PICStaff database row.
    - To create a row in the PICStaff table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            
        - Keys that can be empty strings:
            - "Base Location Names"[index]
            - "MPN"
        
        - Keys that can be empty arrays
            - "Base Location Names"
        
        - Keys that can be Null
            - "Base Location Names"[index]
            - "MPN"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created entry
    
- Update a PICStaff database row.
    - To update a row in the PICStaff table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - "Base Location Names"[index]
            - "MPN"
         
         - Keys that can be empty arrays
            - "Base Location Names"
        
        - Keys that can be Null
            - "Base Location Names"[index]
            - "MPN"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created entry

- Delete a PICStaff database row.
    - To delete a row in the PICStaff table, the value for "db_action" in the JSON Body must equal "delete".
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
    - If there are no errors in the JSON Body document:
        - It contains the key "row", the value for which is "Deleted".
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
### Staff Data Retrieval API
- To retrieve staff data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/staff/
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
                "Email": String,
                "Type": String,
                "Database ID": Integer,
                "County": String,
                "Region": String,
                "First Name": String,
                "Last Name": String,
                "Authorized Credentials": Boolean,
                "Picture": Link,
                "Base Location": [{
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
                "MPN": String,
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


### Staff Picture Edit Page
- To view/change the profile picture for a given staff member, submit a GET request to http://picbackend.herokuapp.com/v2/staff_pic/ with the following Mandatory parameters: "id",