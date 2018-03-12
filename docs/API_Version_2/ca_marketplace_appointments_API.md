## Care Advisors Marketplace Appointment API README


### Marketplace Appointments Retrieval API
- To read rows from the MarketplaceAppointments table, make a GET request to http://picbackend.herokuapp.com/v2/marketplace_appointments/
    - Results will be filtered by the given parameters.
    - Parameters are divided into 2 categories: "primary" and "secondary"
    
    - "Primary" parameters - One and exactly one of these parameters are required in every request.
        - "id" corresponds to ConsumerGeneralConcern class database id.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all staff members.
        - "nav_id" corresponds to navigator table database id.
            - Must be an integer
            - Can be multiple values separated by commas.
    
    - "Secondary" parameters - Any number of these parameters can be added to a request.
        - None
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "id": Integer,
                "date": string,
                "navigator_id": integer,
                "consumer_id": integer,
                "start_time": string,
                "end_time": string
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
    - Eg: If "first_name" is the "Primary" parameter the results will be grouped like the following
        
        ```
        "Data": [
            Results for first_name parameter 2,
            Results for first_name parameter 1,
            Results for first_name parameter 3,
            ...,
        ] (Order is arbitrary)
        ```
        
- If rows are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If rows are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        - Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.