## General Concerns Backend API

### General Concerns Data Submission API
To create, update, or delete rows in the ConsumerGeneralConcern table of the database, make a PUT request to: http://picbackend.herokuapp.com/v2/general_concerns/.

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
 "Data": Object,
}
```

- Create a ConsumerGeneralConcern database row.
    - To create a row in the ConsumerGeneralConcern table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            
        - Keys that can be empty strings:
            - None
            
        - Keys that can be Null
            - None

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a ConsumerGeneralConcern database row.
    - To update a row in the ConsumerGeneralConcern table, the value for "db_action" in the JSON Body must equal "update".
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

- Delete a ConsumerGeneralConcern database row.
    - To delete a row in the ConsumerGeneralConcern table, the value for "db_action" in the JSON Body must equal "delete".
    
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
    
    
### General Concerns Data Retrieval API
- To read rows from the ConsumerGeneralConcern table, make a GET request to http://picbackend.herokuapp.com/v2/general_concerns/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "name" corresponds to general concern name.
            - Must be a String.
            - all non ASCII characters must be url encoded.
        - "id" corresponds to ConsumerGeneralConcern class database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all staff members.
    
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - None
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "name": String,
                "related_specific_concerns": [
                                                {
                                                    "question": String,
                                                    "research_weight": Integer,
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