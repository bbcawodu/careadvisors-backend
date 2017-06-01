## Hospital Web Traffic Data API

### Hospital Web Traffic Data Submission API
To create a HospitalWebTrafficData entry in the database, make a PUT request to: http://picbackend.herokuapp.com/v2/hospital_web_traffic_data/.
- Field 'hospital_name' is unique: Only one HospitalWebTrafficData entry with a given 'hospital_name' field is allowed

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document which has the following format:

```
{
"hospital_name": String,
"monthly_visits": Integer,
"Database ID": Integer(Required when "Database Action" == "Instance Modification" or "Instance Deletion"),
"Database Action": String,
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

- Creating a HospitalWebTrafficData database entry.
    - To create a HospitalWebTrafficData database entry, the value for "Database Action" in the JSON Body must equal "Instance Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key.
        - It contains the key "Database ID", the value for which is the database id of the created entry
    
- Updating a HospitalWebTrafficData database entry.
    - To update a HospitalWebTrafficData database entry, the value for "Database Action" in the JSON Body must equal "Instance Modification".
    - All other fields must be filled.
    - All key value pairs in the JSON Body document correspond to updated fields for specified "Database ID"

- Deleting a HospitalWebTrafficData database entry.
    - To delete a HospitalWebTrafficData database entry, the value for "Database Action" in the JSON Body must equal "Instance Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
### Hospital Web Traffic Data Retrieval API.
- To retrieve hospital web traffic data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/hospital_web_traffic_data/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "hospital_name" corresponds to hospital_name.
            - Must be a string
            - all non ASCII characters must be url encoded
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
                "hospital_name": String,
                "monthly_visits": Integer,
                "consumers_seeking_health_services": Integer,
                "consumers_who_spill_off": Integer,
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
    -Eg: If "name" is the "Primary" parameter the results will be grouped like the following
        
        ```
        "Data": [
            Results for name parameter 2,
            Results for name parameter 1,
            Results for name parameter 3,
            ...,
        ] (Order is arbitrary)
        ```
        
- If hospital web traffic data is found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If metrics reports are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.