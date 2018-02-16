## Navigator Hub Location Backend API


### Navigator Hub Location Data Modification API
To create, update, or delete a row in the NavMetricsLocation table of the database, make a PUT request to: http://picbackend.herokuapp.com/v2/navigator_hub_locations/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"Location Name": String,
"Address Line 1": String,
"Address Line 2": String,
"City": String,
"State": String,
"Zipcode": String,
"Country": String,
"cps_location": Boolean,

"db_action": String,
"id": Integer,
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Create a NavMetricsLocation database row.
    - To create a row in the NavMetricsLocation table, the value for "db_action" in the JSON Body must equal "create".
    
        - Keys that can be omitted:
            - "id"
            
        - Keys that can be empty strings:
            - "address_line_2"
        
        - Keys that can be Null
            - "address_line_2"

    - If there are no errors in the JSON Body document:        
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the created row.
    
- Update a NavMetricsLocation database row.
    - To update a row in the NavMetricsLocation table, the value for "db_action" in the JSON Body must equal "update".
    - All key value pairs in the JSON Body document correspond to updated fields for specified "id"
    - Note: at least one key other than "id" and "db_action" must be present
    
        - Keys that can be omitted:
            - "Location Name"
            - "cps_location"
        
        - Keys that can be empty strings:
            - "address_line_2"
        
        - Keys that can be Null
            - "address_line_2"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is an object with the fields of the updated row.

- Delete a NavMetricsLocation database row.
    - To delete a row in the NavMetricsLocation table, the value for "db_action" in the JSON Body must equal "delete".
    
        - Keys that can be omitted:
            - all except "id" and "db_action"
        
    - If there are no errors in the JSON Body document:
        - The response JSON document will have a dictionary object as the value for the "Data" key.
            - It contains the key "row", the value for which is "Deleted".
    
    
### Navigator Location Data Retrieval API
- To navigator location data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/navigator_hub_locations/
    - Results will be filtered by the given parameters.
    
    - "is_cps_location" corresponds to whether the location is a Chicago Public Schools location.
        - must be of type boolean (true or false)
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {"Name": "Presence Saint Joseph Hospital",
             "Zipcode": "60657",
             "State": "IL",
             "Address Line 1": "2900 N Lake Shore Dr.",
             "Address Line 2": "",
             "Country": "United States of America",
             "City": "Chicago",
             "cps_location": False},
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

- If navigator locations are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If navigator locationss are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.