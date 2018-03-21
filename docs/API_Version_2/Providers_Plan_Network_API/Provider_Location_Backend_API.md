## Healthcare Provider Location Backend API

### Healthcare Provider Location Data Submission API
To create, update, or delete rows in the ProviderLocation table of the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/provider_locations/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
    "name": String,
    "state_province": String (2 letter code),
    "provider_network_id": Integer (Database ID of the Network this location belongs to.),
    "add_accepted_plans": [
        Integer,
        ...,
        ...
    ](List of Database ID's for HealthcarePlan entries),
    "remove_accepted_plans": [
        Integer,
        ...,
        ...
    ](List of Database ID's for HealthcarePlan entries),
    "id": Integer
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

- Create a ProviderLocation database row.
    - To create a row in the ProviderLocation table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "remove_accepted_plans"
            
        - Keys that can be empty strings:
            - "state_province"
        
        - Keys that can be empty arrays
            - "add_accepted_plans"
        
        - Keys that can be Null
            - "provider_network_id"
            - "state_province"
            
        - Keys that WILL NOT be read
            - "remove_accepted_plans"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a ProviderLocation database row.
    - To update a row in the ProviderLocation table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - "state_province"
         
         - Keys that can be empty arrays
            - None
        
        - Keys that can be Null
            - "provider_network_id"
            - "state_province"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a ProviderLocation database row.
    - To delete a row in the ProviderLocation table, the value for "db_action" in the JSON Body must equal "delete".
    
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
    
    
### Healthcare Provider Location Data Retrieval API
- To retrieve ProviderNetwork data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/provider_locations/ with the following optional parameters:
"name", "id"
    - Results will be filtered by the given parameters.
    - NOTE: Only one of the following parameters allowed at a time
    - "name" corresponds to a provider location name.
        - Must be a string
        - all non ASCII characters must be url encoded
    - "id" corresponds to database id of a provider location.
        - passing "all" as the value will return all provider locations.
        - All other cases:
            - must be a base 10 integer.
            - Can be multiple values separated by commas.
    - "network_name" corresponds to a provider network name that a provider location belongs to.
        - Must be a string
        - all non ASCII characters must be url encoded.
    - "state" corresponds to the state of a hospital.
        - must be a string.
        - Must be state's 2 letter code
        - Can be multiple values separated by commas.
    - "network_id" corresponds to database id of a provider network that locations belong to.
        - passing "all" as the value will return all provider locations for all provider networks
        - All other cases:
            - must be a base 10 integer.
            - Can be multiple values separated by commas.
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "name": String,
                "accepted_plans": [1,
                                   2,
                                   Integer,
                                   ...,] (Database ids of accepted plans at this location)
                "Database ID": Integer (Database id for this provider location),
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

- If provider locations are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If provider locations are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.