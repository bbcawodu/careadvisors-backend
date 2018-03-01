## Healthcare Plans Backend API

### Healthcare Plans Data Submission API
To create, update, or delete rows in the HealthcarePlan table of the database, make a PUT request to: http://picbackend.herokuapp.com/v2/plans/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
    "name": String,
    "metal_level": String,
    "premium_type": String,
    "Carrier Database ID": Integer,
    "county" : String,
    
    ### Summary Report Fields
    "medical_deductible_individual_standard": Float,
    "medical_out_of_pocket_max_individual_standard": Float,
    "primary_care_physician_standard_cost": String,
    ###
    
    ### Detailed Report Fields
    "specialist_standard_cost": String,
    "emergency_room_standard_cost": String,
    "inpatient_facility_standard_cost": String,
    "generic_drugs_standard_cost": String,
    "preferred_brand_drugs_standard_cost": String,
    "non_preferred_brand_drugs_standard_cost": String,
    "specialty_drugs_standard_cost": String,
    ###
    
    ### Extra Benefit Information Fields
    "medical_deductible_family_standard": Float,
    "medical_out_of_pocket_max_family_standard": Float,
    ###
    
    "id": Integer,
    "db_action": String,
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

- Create a HealthcarePlan database row.
    - To create a row in the HealthcarePlan table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "medical_deductible_individual_standard"
            - "medical_out_of_pocket_max_individual_standard"
            - "primary_care_physician_standard_cost"
            - "specialist_standard_cost"
            - "emergency_room_standard_cost"
            - "inpatient_facility_standard_cost"
            - "generic_drugs_standard_cost"
            - "preferred_brand_drugs_standard_cost"
            - "non_preferred_brand_drugs_standard_cost"
            - "specialty_drugs_standard_cost"
            - "medical_deductible_family_standard"
            - "medical_out_of_pocket_max_family_standard"
            - "county"
            
        - Keys that can be empty strings:
            - None
        
        - Keys that can be Null
            - "medical_deductible_individual_standard"
            - "medical_out_of_pocket_max_individual_standard"
            - "primary_care_physician_standard_cost"
            - "specialist_standard_cost"
            - "emergency_room_standard_cost"
            - "inpatient_facility_standard_cost"
            - "generic_drugs_standard_cost"
            - "preferred_brand_drugs_standard_cost"
            - "non_preferred_brand_drugs_standard_cost"
            - "specialty_drugs_standard_cost"
            - "medical_deductible_family_standard"
            - "medical_out_of_pocket_max_family_standard"
            - "county"
            
        - Keys that WILL NOT be read
            - "id"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a HealthcarePlan database row.
    - To update a row in the HealthcarePlan table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - None
        
        - Keys that can be Null
            - - "medical_deductible_individual_standard"
            - "medical_out_of_pocket_max_individual_standard"
            - "primary_care_physician_standard_cost"
            - "specialist_standard_cost"
            - "emergency_room_standard_cost"
            - "inpatient_facility_standard_cost"
            - "generic_drugs_standard_cost"
            - "preferred_brand_drugs_standard_cost"
            - "non_preferred_brand_drugs_standard_cost"
            - "specialty_drugs_standard_cost"
            - "medical_deductible_family_standard"
            - "medical_out_of_pocket_max_family_standard"
            - "county"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a HealthcarePlan database row.
    - To delete a row in the HealthcarePlan table, the value for "db_action" in the JSON Body must equal "delete".
    
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
    
    
### Healthcare Plan Data Retrieval API
- To retrieve HealthcarePlan data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/plans/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
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
        - "accepted_location_id" corresponds to database id of a provider location that a plan is accepted at.
            - passing "all" as the value will return all plans that are accepted for all provider locations
            - All other cases:
                - must be a base 10 integer.
                - Can be multiple values separated by commas.
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - "include_summary_report" corresponds to whether to include the summary report for each plan if it exists.
            - must be of type boolean (true or false)
        - "include_detailed_report" corresponds to whether to include the detailed report for each plan if it exists.
            - must be of type boolean (true or false)
        - "premium_type" - Premium type of a given plan.
            - Must be one of the following values: ['HMO', 'PPO', 'POS', 'EPO']
            - Must be a string
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