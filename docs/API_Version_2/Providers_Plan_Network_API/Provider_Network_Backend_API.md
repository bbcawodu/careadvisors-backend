## Healthcare Provider Network Backend API

### Healthcare Provider Network Data Submission API
To create, update, or delete members of the ProviderNetwork class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/provider_networks/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"name": String,
"Database ID": Integer(Required when "Database Action" == "Provider Network Modification" or "Provider Network Deletion"),
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

- Creating a ProviderNetwork database entry.
    - To create a ProviderNetwork database entry, the value for "Database Action" in the JSON Body must equal "Provider Network Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Updating a ProviderNetwork database entry.
    - To update a ProviderNetwork database entry, the value for "Database Action" in the JSON Body must equal "Provider Network Modification".
    - All other fields must be filled.
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"

- Deleting a ProviderNetwork database entry.
    - To delete a ProviderNetwork database entry, the value for "Database Action" in the JSON Body must equal "Provider Network Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
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