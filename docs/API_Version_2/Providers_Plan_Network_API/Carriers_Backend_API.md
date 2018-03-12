## Healthcare Carriers Backend API

### Healthcare Carrier Data Submission API
To create, update, or delete rows in the HealthcareCarrier table of the database, make a PUT request to: http://picbackend.herokuapp.com/v2/carriers/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"name": String,
"state_province": String (Must be a valid State Abbreviation eg. TX),

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
            "Errors": Array,
            "Warnings": Array,
           },
 "Data": Dictionary Object or "Deleted",
}
```

- Create a HealthcareCarrier database row.
    - To create a row in the HealthcareCarrier table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that WILL NOT be read
            - "id"
            
        - Keys that can be empty strings:
            - None
        
        - Keys that can be Null
            - None

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a HealthcareCarrier database row.
    - To update a row in the HealthcareCarrier table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - None
        
        - Keys that can be Null
            - None
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a HealthcareCarrier database row.
    - To delete a row in the HealthcareCarrier table, the value for "db_action" in the JSON Body must equal "delete".
    
        - Keys that WILL NOT be read
            - all except "id" and "db_action"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is "Deleted".
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### Healthcare Carrier Data Retrieval API
- To retrieve HealthcareCarrier data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/carriers/ with the following optional parameters: "name", "id", "state"
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "name" corresponds to carrier name.
            - Must be a string
            - all non ASCII characters must be url encoded
        - "id" corresponds to database id.
            - passing "all" as the value will return all carriers
            - All other cases:
                - must be a base 10 integer.
                - Can be multiple values separated by commas.
        - "state" corresponds to the coverage state of a carrier.
            - must be a string.
            - Can be multiple values separated by commas.
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - "has_sample_id_card" corresponds to whether HealthcareCarrier object has a non default sample id card image.
            - must be of type boolean (true or false
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "name": String,
                "Database ID": Integer,
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
    -Eg: If "name" is the "Primary" parameter the results will be grouped like the following
        
        ```
        "Data": [
            Results for name parameter 2,
            Results for name parameter 1,
            Results for name parameter 3,
            ...,
        ] (Order is arbitrary)
        ```
        
        
- If healthcare carriers are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If healthcare carriers are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
    
    
### Healthcare Carrier Sample id card upload page.
- To view/change the sample id card for a HealthcareCarrier entry in the database, submit a GET request to http://picbackend.herokuapp.com/v2/carrier_sample_id_card_manager/ with the following mandatory parameter, "id".