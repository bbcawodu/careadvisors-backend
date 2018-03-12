## Healthcare Provider Network Backend API

### Healthcare Provider Network Data Submission API
To create, update, or delete rows in the ProviderNetwork table in the database, make a PUT request to: http://picbackend.herokuapp.com/v2/provider_networks/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
    "name": String,
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

- Create a ProviderNetwork database row.
    - To create a row in the PICConsumer table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - None
            
        - Keys that can be empty strings:
            - None
        
        - Keys that can be Null
            - None
            
        - Keys that WILL NOT be read
            - "id"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a ProviderNetwork database row.
    - To update a row in the ProviderNetwork table, the value for "db_action" in the JSON Body must equal "update".
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
         
         - Keys that can be empty arrays
            - "consumer_notes"
            - cps_info["secondary_dependents"]
        
        - Keys that can be Null
            - "date_met_nav"
            - "cps_info"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a ProviderNetwork database row.
    - To delete a row in the ProviderNetwork table, the value for "db_action" in the JSON Body must equal "delete".
    
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
    
    
### Healthcare Provider Network Data Retrieval API
- To retrieve ProviderNetwork data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/provider_networks/ with the following optional parameters:
"name", "id"
    - Results will be filtered by the given parameters.
    - NOTE: Only one of the following parameters allowed at a time
    - "name" corresponds to a provider network name.
        - Must be a string
        - all non ASCII characters must be url encoded
    - "id" corresponds to database id of a provider network.
        - passing "all" as the value will return all provider networks.
        - All other cases:
            - must be a base 10 integer.
            - Can be multiple values separated by commas.
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "name": String,
                "provider_locations": [1,
                                       2,
                                       Integer,
                                       ...,] (Database ids for provider locations in this network.)
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

- If provider networks are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If provider networks are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.