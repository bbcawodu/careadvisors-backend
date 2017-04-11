## Navigator Hub Location Backend API


### Navigator Hub Location Data Modification API
To modify or add navigator hub locations in the database programatically, submit a PUT request to: http://picbackend.herokuapp.com/v2/navigator_hub_locations/.

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
"Database Action": String

"cps_location": Boolean (Key may be omitted)
"Database ID": Integer(Required when "Database Action" == "Staff Modification" or "Staff Deletion"),
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

- Adding a navigator hub location database entry.
    - To add a navigator hub location database entry, the value for "Database Action" in the JSON Body must equal "Location Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Modifying a navigator hub location database entry.
    - To modify a navigator hub location database entry, the value for "Database Action" in the JSON Body must equal "Location Modification".
    - All other fields must be filled.
    - All key value pairs in the JSON Body document correspond to updated fields for specified "Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the updated entry

- Deleting a navigator hub location database entry.
    - To delete a navigator hub location database entry, the value for "Database Action" in the JSON Body must equal "Location Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### Navigator Location Data Retrieval API
- To navigator location data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/navigator_hub_locations/
    
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