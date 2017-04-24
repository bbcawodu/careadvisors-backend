## Healthcare Provider Location Backend API

### Healthcare Provider Location Data Submission API (IN DEVELOPMENT)
To create, update, or delete members of the ProviderLocation class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/provider_locations/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"name": String,
"provider_network Database ID": Integer(Database ID for ProviderNetwork entry),
"accepted_plans": [Integer,
                   ...,
                   ...
                  ](List of Database ID's for HealthcarePlan entries),
"Network Database ID": Integer (Database ID of the Network this location belongs to.),
"Database ID": Integer(Required when "Database Action" == "Modify Provider Location", "Modify Provider Location - add_accepted_plans"),
               "Modify Provider Location - delete_accepted_plans", or "Delete Provider Location"
"Database Action": String,
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

- Creating a ProviderLocation database entry.
    - To create a ProviderLocation database entry, the value for "Database Action" in the JSON Body must equal "Add Provider Location".
    - All other fields except "Database ID" must be filled.
    - accepted_plans list information
        - Must contain database ids for valid Healthcare Plan entries
        - The ProviderLocation entry will have an accepted_plans list that EXACTLY matches the given list.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Updating a ProviderLocation database entry.
    - To update a ProviderLocation database entry, the value for "Database Action" in the JSON Body must equal "Modify Provider Location".
    - All other fields must be filled.
    - accepted_plans list information
        - Must contain database ids for valid Healthcare Plan entries
        - The ProviderLocation entry will have an accepted_plans list that EXACTLY matches the given list.
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"
    
- Updating a ProviderLocation database entry - Adding an accepted plan.
    - To update a ProviderLocation database entry, the value for "Database Action" in the JSON Body must equal "Modify Provider Location - add_accepted_plans".
    - All other fields must be filled.
    - accepted_plans list information
        - Must contain database ids for valid Healthcare Plan entries
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"
    
- Updating a ProviderLocation database entry - Deleting an accepted plan.
    - To update a ProviderLocation database entry, the value for "Database Action" in the JSON Body must equal "Modify Provider Location - delete_accepted_plans".
    - All other fields must be filled.
    - accepted_plans list information
        - Must contain database ids for valid Healthcare Plan entries
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"

- Deleting a ProviderLocation database entry.
    - To delete a ProviderLocation database entry, the value for "Database Action" in the JSON Body must equal "Delete Provider Location".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### Healthcare Provider Location Data Retrieval API (IN DEVELOPMENT)
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
        - all non ASCII characters must be url encoded
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