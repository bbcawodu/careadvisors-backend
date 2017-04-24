## Healthcare Plans Backend API

### Healthcare Plans Data Submission API
To create, update, or delete members of the HealthcarePlan class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/plans/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"name": String,
"metal_level": String,
"premium_type": String,
"Carrier Database ID": Integer (Database ID of the Carrier for this plan),
"Database ID": Integer(Required when "Database Action" == "Plan Modification" or "Plan Deletion"),
"Database Action": String,
}
```

The Following is a list of possible values for the "premium_type" field along with corresponding model constants:
```
[
    HMO = "HMO"
    PPO = "PPO"
    POS = 'POS'
    EPO = 'EPO'
]
```

The Following is a list of possible values for the "metal_level" field along with corresponding model constants:
```
[
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = 'Platinum'
    CATASTROPHIC = "Catastrophic"
]
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

- Creating a HealthcarePlan database entry.
    - To create a HealthcarePlan database entry, the value for "Database Action" in the JSON Body must equal "Plan Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Updating a HealthcarePlan database entry.
    - To update a HealthcarePlan database entry, the value for "Database Action" in the JSON Body must equal "Plan Modification".
    - All other fields must be filled.
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"

- Deleting a HealthcarePlan database entry.
    - To delete a HealthcarePlan database entry, the value for "Database Action" in the JSON Body must equal "Plan Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### Healthcare Plan Data Retrieval API
- To retrieve HealthcarePlan data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/plans/ with the following optional parameters:
"name", "id", "carrier_id", "carrier_name", "carrier_state"
    - Results will be filtered by the given parameters.
    - NOTE: Only one of the following parameters allowed at a time
    - "name" corresponds to the plan name.
        - Must be a string
        - all non ASCII characters must be url encoded
    - "id" corresponds to database id.
        - passing "all" as the value will return all plans
        - All other cases:
            - must be a base 10 integer.
            - Can be multiple values separated by commas.
    - "carrier_id" corresponds to the database id of plan carriers.
        - passing "all" as the value will return plans for all carriers in the db.
        - All other cases:
            - must be a base 10 integer.
            - Can be multiple values separated by commas.
    - "carrier_name" corresponds to the carrier name.
        - Must be a string
        - all non ASCII characters must be url encoded
    - "carrier_state" corresponds to the state that a carrier operates in.
        - Must be a string
        - all non ASCII characters must be url encoded
        - Can be multiple values separated by commas.
        - Return value will be a list of lists. One list for each state requested.
    - "accepted_location_id" corresponds to database id of a provider location that a plan is accepted at. (IN DEVELOPMENT)
        - passing "all" as the value will return all plans that are accepted for all provider locations
        - All other cases:
            - must be a base 10 integer.
            - Can be multiple values separated by commas.
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "name": String,
                "premium_type": String,
                "metal_level": String,
                "carrier_info": {"name": String,
                                 "state": String,
                                 "Database ID": Integer},
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

- If healthcare plans are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If healthcare plans are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.