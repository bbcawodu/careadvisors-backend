# Follow Up Notices Backend API README (IN DEVELOPMENT)


## Entity Relationship Diagram for Follow Up Notices related data models

![Follow Up Notices Entity Relationship Diagram](follow_up_notices_erd.jpg)


### Modify Follow Up Notices Table Rows (IN DEVELOPMENT)
To create, update, or delete a row in the FollowUpNotices table of the database, make a PUT request to: http://picbackend.herokuapp.com/v2/cm_follow_up_notices/.

- The headers of the request MUST include: 
    - "Content-Type: "application/json""
    - "X-Requested-With: "XMLHttpRequest"""
    
The body of the request must be a JSON document using the following template:

```
{
    "consumer_id": Integer (id of row in PICConsumers table),
    "navigator_id": Integer (id of row in Navigators table),
    
    "status": String,
    "severity": String,
    "notes": String,
    
    "db_action": String,
    "id": Integer,
}
```

The Following is a list of possible "status" values with corresponding model constant names:
```
[
    N_A = "not available",
    OPEN = "Open",
    COMPLETED = "Completed",
]
```

The Following is a list of possible "severity" values with corresponding model constant names:
```
[
    N_A = "not available",
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "HIGH"
    URGENT = "Urgent"
]
```

In response, a JSON document will be displayed with the following format:
```
{
    "Status":
        {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array
            "Data": Object or "Deleted",
        }
}
```

- Create a FollowUpNotices database row.
    - To create a row in the FollowUpNotices table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            - "notes"
            
        - Keys that can be empty strings:
            - "status"
            - "severity"
            - "notes"
        
        - Keys that can be Null
            - "status"
            - "severity"
            - "notes"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a FollowUpNotices database row.
    - To update a row in the FollowUpNotices table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
        - Keys that can be empty strings:
            - "status"
            - "severity"
            - "notes"
        
        - Keys that can be Null
            - "status"
            - "severity"
            - "notes"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a FollowUpNotices database row.
    - To delete a row in the FollowUpNotices table, the value for "db_action" in the JSON Body must equal "delete".
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is "Deleted".
    
    
### Follow Up Notices Data Retrieval API (IN DEVELOPMENT)
- To read rows from the FollowUpNotices table of the backend, make a GET request to http://picbackend.herokuapp.com/v2/cm_follow_up_notices/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "id" corresponds to database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all staff members.
            
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - "nav_id" corresponds to the Navigators table database id.
            - Must be an integer
            - Can be multiple values separated by commas.
        - "consumer_id" corresponds to the PICConsumer table database id.
            - Must be an integer
            - Can be multiple values separated by commas.
        - "status" corresponds to the status column.
            - Must be an ascii string that has all non-ascii characters url encoded
        - "severity" corresponds to the severity column.
            - Must be an ascii string that has all non-ascii characters url encoded
        - "date_created_start" - Start date of the date_created field (inclusive)
            - Must be given in "YYYY-MM-DD" format
        - "date_created_end" - End date of the date_created field (inclusive)
            - Must be given in "YYYY-MM-DD" format
        - "date_modified_start" - Start date of the date_modified field (inclusive)
            - Must be given in "YYYY-MM-DD" format
        - "date_modified_end" - End date of the date_modified field (inclusive)
            - Must be given in "YYYY-MM-DD" format
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "consumer": Integer,
                "navigator": Integer,
                
                "status": String,
                "severity": String,
                "notes": String,
                
                "id": Integer,
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

- If FollowUpNotices table rows are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If FollowUpNotices table rows are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
