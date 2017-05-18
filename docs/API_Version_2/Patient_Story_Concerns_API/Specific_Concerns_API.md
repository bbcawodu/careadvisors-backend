## Specific Concerns Backend API

### Specific Concerns Data Submission API
To create, update, or delete members of the ConsumerSpecificConcern class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/specific_concerns/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"question": String,
"related_general_concerns": [
                                Integer,
                                ...,
                                ...
                            ],
"research_weight": Integer(Can be omitted. iIf omitted, will be set to a default value of 50),
"Database ID": Integer(Required when "Database Action" == "Modify Specific Concern", "Modify Specific Concern - add_general_concern"),
               "Modify Specific Concern - remove_general_concern", or "Delete Specific Concern"
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

- Creating a ConsumerSpecificConcern database entry.
    - To create a ConsumerSpecificConcern database entry, the value for "Database Action" in the JSON Body must equal "Add Specific Concern".
    - All other fields except "Database ID" must be filled.
    - related_general_concerns list information
        - Must contain names of specific concerns that already exist as ConsumerGeneralConcern entries in the db.
        - The ConsumerSpecificConcern entry will have an related_general_concerns list that EXACTLY matches the given list.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Updating a ConsumerSpecificConcern database entry.
    - To update a ConsumerSpecificConcern database entry, the value for "Database Action" in the JSON Body must equal "Modify Specific Concern".
    - All other fields must be filled.
    - related_general_concerns list information
        - Must contain names of specific concerns that already exist as ConsumerGeneralConcern entries in the db.
        - The ConsumerSpecificConcern entry will have an related_general_concerns list that EXACTLY matches the given list.
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"
    
- Updating a ConsumerSpecificConcern database entry - Adding an accepted plan.
    - To update a ConsumerSpecificConcern database entry, the value for "Database Action" in the JSON Body must equal "Modify Specific Concern - add_general_concern".
    - All other fields must be filled.
    - related_general_concerns list information
        - Must contain names of specific concerns that already exist as ConsumerGeneralConcern entries in the db.
        - All given values will be added to the related_general_concerns list of the current ConsumerSpecificConcern.
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"
    
- Updating a ConsumerSpecificConcern database entry - Removing an accepted plan.
    - To update a ConsumerSpecificConcern database entry, the value for "Database Action" in the JSON Body must equal "Modify Specific Concern - remove_general_concern".
    - All other fields must be filled.
    - related_general_concerns information
        - Must contain names of specific concerns that already exist as ConsumerGeneralConcern entries in the db.
        - All given values will be removed from the related_general_concerns list of the current ConsumerSpecificConcern.
    - All key value pairs in the JSON Body correspond to updated fields of the entry for specified "Database ID"

- Deleting a ConsumerSpecificConcern database entry.
    - To delete a ConsumerSpecificConcern database entry, the value for "Database Action" in the JSON Body must equal "Delete Specific Concern".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
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