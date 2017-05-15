## Staff Account Backend API

### Staff Data Submission API
To modify or add members of the PICStaff class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/staff/. 

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
"Base Location Names": [Strings (Can be None or empty string)], # If any locations are not found, an error will be added and the staff member will still be saved
"MPN": String(Can be None or empty string),
"Database ID": Integer(Required when "Database Action" == "Staff Modification" or "Staff Deletion"),
"Database Action": String,
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

- Adding a staff member database entry.
    - To add a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Modifying a staff member database entry.
    - To modify a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Modification".
    - All other fields must be filled.
    - All key value pairs in the JSON Body document correspond to updated fields for specified "Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the updated entry

- Deleting a staff member database entry.
    - To delete a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
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
        - "fname" corresponds to first name.
            - Must be a string
            - Can be multiple values separated by commas.
        - "lname" corresponds to last name.
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
        - "id" corresponds to database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all staff members.
        - SPECIAL CASE: Only "fname" and "lname" can be given simultaneously as parameters.
            - When "fname" and "lname" are given at the same time, only one value of each permitted.
            
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