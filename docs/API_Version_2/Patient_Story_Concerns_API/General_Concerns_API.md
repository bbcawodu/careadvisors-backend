## General Concerns Backend API

### General Concerns Data Submission API
To create, update, or delete members of the ConsumerGeneralConcern class in the database, submit a PUT request to: http://picbackend.herokuapp.com/v2/general_concerns/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"name": String,
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

- Creating a ConsumerGeneralConcern database entry.
    - To create a ConsumerGeneralConcern database entry, the value for "Database Action" in the JSON Body must equal "Concern Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Updating a ConsumerGeneralConcern database entry.
    - To update a HealthcareCarrier database entry, the value for "Database Action" in the JSON Body must equal "Concern Modification".
    - All other fields must be filled.
    - All key value pairs in the JSON Body document correspond to updated fields for specified "Database ID"

- Deleting a ConsumerGeneralConcern database entry.
    - To delete a HealthcareCarrier database entry, the value for "Database Action" in the JSON Body must equal "Concern Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### General Concerns Data Retrieval API
- To retrieve ConsumerGeneralConcern data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/general_concerns/
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