## Healthcare Carriers Backend API

### Healthcare Carrier Data Submission API
To create, update, or delete members of the HealthcareCarrier class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/carriers/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"name": String,
"state_province": String (Must be a valid State Abbreviation eg. TX),
"Database ID": Integer(Required when "Database Action" == "Carrier Modification" or "Carrier Deletion"),
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

- Creating a HealthcareCarrier database entry.
    - To create a HealthcareCarrier database entry, the value for "Database Action" in the JSON Body must equal "Carrier Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Updating a HealthcareCarrier database entry.
    - To update a HealthcareCarrier database entry, the value for "Database Action" in the JSON Body must equal "Carrier Modification".
    - All other fields must be filled.
    - All key value pairs in the JSON Body document correspond to updated fields for specified "Database ID"

- Deleting a HealthcareCarrier database entry.
    - To delete a HealthcareCarrier database entry, the value for "Database Action" in the JSON Body must equal "Carrier Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### Healthcare Carrier Data Retrieval API
- To retrieve HealthcareCarrier data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/carriers/ with the following optional parameters: "name", "id", "state"
    - NOTE: Only one of the following parameters allowed at a time
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

- If healthcare carriers are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If healthcare carriers are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.