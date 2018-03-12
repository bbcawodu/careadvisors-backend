## Healthcare Subsidy Eligibility Data By Family Size API (IN DEVELOPMENT)

### Healthcare Subsidy Eligibility Data Submission API (IN DEVELOPMENT)
To create, update, or delete a row in the HealthcareSubsidyEligibilityByFamSize table of the database, make a PUT request to: http://picbackend.herokuapp.com/v2/subsidy_data_by_family_size/.
- Field 'family_size' Information
    - Is unique: Only one HealthcareSubsidyEligibilityByFamSize row with a given 'family_size' value is allowed
    - 'family_size' must be > 0
    

- The headers of the request should include: 
    - "Content-Type: "application/json"
    
The body of the request should be a JSON document which has the following format:

```
{
"family_size": Integer,
"medicaid_income_limit": Float,
"tax_cred_for_marketplace_income_limit": Float,
"marketplace_without_subsidies_income_level": Float,

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
           }
}
```

- Create a HealthcareSubsidyEligibilityByFamSize database row.
    - To create a row in the HealthcareSubsidyEligibilityByFamSize table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            
        - Keys that can be empty strings:
            - None
        
        - Keys that can be Null
            - None
            
        - Keys that WILL NOT be read
            - "id"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a HealthcareSubsidyEligibilityByFamSize database row.
    - To update a row in the HealthcareSubsidyEligibilityByFamSize table, the value for "db_action" in the JSON Body must equal "update".
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

- Delete a HealthcareSubsidyEligibilityByFamSize database row.
    - To delete a row in the HealthcareSubsidyEligibilityByFamSize table, the value for "db_action" in the JSON Body must equal "delete".
    
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
    
### Healthcare Subsidy Eligibility Data Retrieval API (IN DEVELOPMENT)
- To retrieve healthcare subsidy eligibility data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/subsidy_data_by_family_size/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "family_size" corresponds to hospital_name.
            - Must be a integer
            - Can be multiple values separated by commas.
        - "id" corresponds to HospitalTrafficData class database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all HospitalTrafficData entries.
    
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - None
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "family_size": Integer,
                "medicaid_income_limit": Float,
                "tax_cred_for_marketplace_income_limit": Float,
                "marketplace_without_subsidies_income_level": Float,
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
    -Eg: If "family_size" is the "Primary" parameter the results will be grouped like the following
        
        ```
        "Data": [
            Results for family_size parameter 2,
            Results for family_size parameter 1,
            Results for family_size parameter 3,
            ...,
        ] (Order is arbitrary)
        ```
        
- If healthcare subsidy eligibility data is found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If healthcare subsidy eligibility data is not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.