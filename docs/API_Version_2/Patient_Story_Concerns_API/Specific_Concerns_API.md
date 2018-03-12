## Specific Concerns Backend API (IN MAINTENANCE)

### Specific Concerns Data Submission API
To create, update, or delete rows in the ConsumerSpecificConcern Table of the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/specific_concerns/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
    "question": String,
    "add_related_general_concerns": [
        String,
        ...,
        ...
    ],
    "remove_related_general_concerns": [
        String,
        ...,
        ...
    ],
    "research_weight": Integer,
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

- Create a ConsumerSpecificConcern database row.
    - To create a row in the ConsumerSpecificConcern table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            - "research_weight"
            - "add_related_general_concerns"
            
        - Keys that can be empty strings:
            - None
        
        - Keys that can be empty arrays
            - "add_related_general_concerns"
            
        - Keys that WILL NOT be read
            - "remove_related_general_concerns"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a ConsumerSpecificConcern database row.
    - To update a row in the ConsumerSpecificConcern table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - None
         
         - Keys that can be empty arrays
            - None
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a ConsumerSpecificConcern database row.
    - To delete a row in the ConsumerSpecificConcern table, the value for "db_action" in the JSON Body must equal "delete".
    
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
    
    
### Specific Concerns Data Retrieval API
- To retrieve ConsumerSpecificConcern data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/specific_concerns/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "question" corresponds to specific concern question.
            - Must be a String.
            - all non ASCII characters must be url encoded.
        - "id" corresponds to ConsumerSpecificConcern class database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all general concerns.
        - "gen_concern_id" corresponds to a ConsumerGeneralConcern class database id that a "specific concern" is related to.
            - Retrieves specific concerns whose "related_general_concerns" contain the ConsumerGeneralConcern's specified by the  given "gen_concern_id"'s
            - Must be an integer
            - Can be multiple values separated by commas.
        - "gen_concern_id_subset" corresponds to a set of ConsumerGeneralConcern class database id's that a "specific concern"'s "related_general_concerns" is a superset of.
            - Retrieves specific concerns whose "related_general_concerns" are a superset of the ConsumerGeneralConcern's specified by the  given "gen_concern_id"'s
            - Must be an integer
            - Can be multiple values separated by commas.
        - "gen_concern_name" corresponds to a general concern name that a "specific concern" is related to.
            - Retrieves specific concerns whose "related_general_concerns" contain a ConsumerGeneralConcern specified by the given "gen_concern_name"
            - Must be a String.
            - all non ASCII characters must be url encoded.
    
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - None
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "question": String,
                "related_general_concerns": [
                                                {
                                                    "name": String,
                                                    "Database ID": Integer
                                                },
                                                ...,
                                                ...
                                             ] or Null,
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
    -Eg: If "first_name" is the "Primary" parameter the results will be grouped like the following
        
        ```
        "Data": [
            Results for first_name parameter 2,
            Results for first_name parameter 1,
            Results for first_name parameter 3,
            ...,
        ] (Order is arbitrary)
        ```
        
- If ConsumerGeneralConcerns are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If ConsumerGeneralConcerns are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.