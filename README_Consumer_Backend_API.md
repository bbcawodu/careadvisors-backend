## Consumer Account Backend API

### Consumer Data Submission API
To modify or add members of the PICConsumer class in the database, submit a POST request to: http://picbackend.herokuapp.com/editconsumer/. The POST data a JSON document using the following template:

```
{
"First Name": String,
"Middle Name": String (Can be empty),
"Last Name": String,
"Email": String (Can be empty),
"Phone Number": String (Can be empty),
"Met Navigator At": String,
"Household Size": Integer,
"Navigator Notes": [
                        "These are",
                        "sample notes",
                        "navigators write about consumers",
                        ...
                    ](Can be an empty array),
"Plan": String (Can be empty),
"Preferred Language": String (Can be empty),
"Navigator Database ID": Integer,

Address(Every field within address can be given as an empty string. Address will only be recorded/updated iff a full address is given)
"Address Line 1": String (Can be empty),
"Address Line 2": String (Can be empty),
"City": String (Can be empty),
"State": String (Can be empty),
"Zipcode": String (Can be empty),
"date_met_nav":(Can be Null) or {"Day": Integer,
                                "Month": Integer,
                                "Year": Integer,},

"Consumer Database ID": Integer(Required when "Database Action" == "Consumer Modification" or "Consumer Deletion"),
"Database Action": String,
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Adding a consumer database entry.
    - To add a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Addition".
    - All other fields except "Consumer Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the added database entry.
    
- Modifying a consumer database entry.
    - To modify a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Modification".
    - All other fields must be filled.
    - All key value pairs in the POSTed JSON document correspond to updated fields for specified "Consumer Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the updated database entry.

- Deleting a consumer database entry.
    - To delete a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Deletion".
    - The only other field should be "Consumer Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Consumer Data Retrieval API
- To retrieve consumer data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/consumers? with the following parameters(at least one required)
    - A maximum of 20 consumer records with full fields will be returned due to size constraints
        - The rest are consumer database IDs
        - Links to pages with the rest of the full records for your query will be given if you request without "page" parameter
    - "fname" corresponds to consumer first name.
    - "lname" corresponds to consumer last name.
        - "fname" and "lname" can be given simultaneously as parameters. If so, only one value each is permitted.
    - "email" corresponds to consumer email.
    - "region" corresponds to consumer region.
    - "id" corresponds to consumer class database id.
        - passing "all" as the value will return all staff members
    - "navid" corresponds to staff member class database id. (Can be combined with any of the above parameters)
    - "page" corresponds to the current page of consumer instances to be displayed with full fields. 
        - if this parameter is missing, the first 20 consumer instances will be displayed with full fields.
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Email": String,
                "Phone Number": String,
                "Database ID": Integer,
                "Preferred Language": String,
                "First Name": String,
                "Middle Name": String,
                "Last Name": String,
                "date_met_nav": String (Can be Null),
                "Navigator": String,
                "Navigator Notes": [
                                        "These are",
                                        "sample notes",
                                        "navigators write about consumers",
                                        ...
                                    ],
                "Met Navigator At": String,
                "Household Size": Integer,
                "Plan": String,
                "Best Contact Time": String,
                "address": Will either be None or a dictionary of the following form:
                           {
                            "Address Line 1": String,
                            "Address Line 2": String,
                            "City": String,
                            "State": String,
                            "Zipcode": String,
                            "Country": String,
                           }
            },
            ...,
            ...,
            ...,
            up to 20 full record consumer entries,
            2(Database IDs for the rest),
            6,
            9
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        },
        "Page URLs": Array of strings (Will be missing if "page" parameter is given OR less than 20 consumers in results)
    }
    ```

- If consumers are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If consumers are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.
- If "page" parameter is missing and there is more than one page of customer instances to display with all fields, "Page
    URLs" key will be present in the root response dictionary. 