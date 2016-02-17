# Consumer Metrics and Appointments Backend

This is the code for the backend component of our metrics and appointments apps. It enables the API that transmits data between the frontend and the backend.



## Installation

This app runs on a django installation hosted on Heroku. To install Heroku for code editing, go to: https://devcenter.heroku.com/articles/getting-started-with-python#introduction and follow the instructions for your particular operating system.



## Presence Healthcare Appointment Scheduler Backend

### Presence Healthcare Appointment Addition API
To add an appointment to the database using our appointments API, make a POST request to: http://obscure-harbor-6074.herokuapp.com/submitappointment/. The POST data should be a JSON document which has the following format:

```
{
 "First Name": String,
 "Last Name": String,
 "Email": String,
 "Phone Number": String,
 "Preferred Language": String (Not Required),
 "Best Contact Time": String (Not Required),
 "Appointment": {
                 "Name": String,
                 "Street Address": String,
                 "City": String,
                 "State": String,
                 "Zip Code": String,
                 "Phone Number": String,
                 "Appointment Slot": {
                                      "Date": {
                                               "Month": Integer,
                                               "Day": Integer,
                                               "Year": Integer
                                              },
                                      "Start Time": {
                                                     "Hour": Integer,
                                                     "Minutes": Integer
                                                    },
                                      "End Time": {
                                                   "Hour": Integer,
                                                   "Minutes": Integer
                                                  }
                                     },
                 "Point of Contact": {
                                      "First Name": String,
                                      "Last Name": String,
                                      "Email": String,
                                      "Type": String
                                     }
                }
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
           }
}
```

- If there are no errors in the POSTed JSON doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "status" dictionary.
    - An instance of the Appointment class corresponding to the POSTed JSON doc will be created and saved in the database.
        - If there isn't a consumer database entry with an email field corresponding to the POST, one is created.
        - If there isn't a location database entry with a name field corresponding to the POST, one is created.
        - If there isn't a staff database entry with an email field corresponding to the POST, one is created.
    
- If there are errors in the POSTed JSON doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "status" dictionary.
        - Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.



### Presence Healthcare Appointments Viewer
Go to http://obscure-harbor-6074.herokuapp.com/viewappointments to view what appointments have been submitted by consumers and to whom they have been assigned.



## Staff Account Backend API

### Staff Data Submission API
To modify or add members of the PICStaff class in the database, submit a POST request to: http://obscure-harbor-6074.herokuapp.com/editstaff/. The POST data a JSON document using the following template:

```
{
"First Name": String,
"Last Name": String,
"Email": String,
"User Type": String,
"User County": String,
"Database ID": Integer(Required when "Database Action" == "Staff Modification" or "Staff Deletion"),
"Database Action": String,
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Adding a staff member database entry.
    - To add a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the added database entry.
    
- Modifying a staff member database entry.
    - To modify a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Modification".
    - All other fields must be filled.
    - All key value pairs in the POSTed JSON document correspond to updated fields for specified "Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the updated database entry.

- Deleting a staff member database entry.
    - To delete a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Staff Data Retrieval API
- To retrieve staff data stored in the backend, submit a GET request to http://obscure-harbor-6074.herokuapp.com/v1/staff? with the following optional parameters: "fname", "lname", "email", "id"
    - "fname" corresponds to first name.
    - "lname" corresponds to last name.
    - "email" corresponds to email.
    - "id" corresponds to database id.
        - passing "all" as the value will return all staff members
    - All parameters may have a single or multiple values separated by commas
    - One parameter is allowed at a time (only "fname" and "lname" can be grouped)
        - If "fname" and "lname" are given simultaneously as parameters, only one value each is permitted.
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Email": String,
                "Type": String,
                "Database ID": Integer,
                "County": String,
                "First Name": String,
                "Last Name": String
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- If staff members are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If staff members are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.



## Consumer Metrics Backend API

### Consumer Metrics Submission API
To submit an entry of consumer metrics data corresponding to a specific staff member, make a POST request to: http://obscure-harbor-6074.herokuapp.com/submitmetrics/. The POST data should be a JSON document which has the following format:

```
{
"Email": String,
"User Type": "IPC" or "Navigator",
"Consumer Metrics": {"Metrics Date":{"Day": Integer,
                                    "Month": Integer,
                                    "Year": Integer,},
                    "County": String,
                    "Received Education": Integer,
                    "Applied Medicaid": Integer,
                    "Selected QHP": Integer,
                    "Enrolled SHOP": Integer,
                    "Referred Medicaid or CHIP": Integer,
                    "Referred SHOP": Integer,
                    "Filed Exemptions": Integer,
                    "Received Post-Enrollment Support": Integer,
                    "Trends": String (Not Required),
                    "Success Story": String,
                    "Hardship or Difficulty": String,
                    "Comments": String (Not Required),
                    "Outreach and Stakeholder Activities": String (Not Required),
                    //////// IPC Questions /////////
                    "Appointments Scheduled": Integer,
                    "Confirmation Calls": Integer,
                    "Appointments Held": Integer,
                    "Appointments Over Hour": Integer,
                    "Appointments Complex Market": Integer,
                    "Appointments Complex Medicaid": Integer,
                    "Appointments Post-Enrollment Assistance": Integer,
                    "Appointments Over 3 Hours": Integer,
                    }
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
           }
}
```

- If there are no errors in the POSTed JSON doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "status" dictionary.
    - An instance of the MetricsSubmission class corresponding to the POSTed JSON doc will be created and saved in the database.
        - Only one metrics submission is allowed per day.
    
- If there are errors in the POSTed JSON doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "status" dictionary.
        - Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Consumer Metrics Retrieval API.
- To retrieve metrics data stored in the backend, submit a GET request to http://obscure-harbor-6074.herokuapp.com/v1/metrics? with the following optional parameters: "fname", "lname", "email", "id", "county", "time", "groupby"
    - "fname" corresponds to staff member first name.
    - "lname" corresponds to staff member last name.
    - "email" corresponds to staff member email.
    - "id" corresponds to staff member class database id.
        - passing "all" as the value will return all staff members
    - "county" corresponds to counties that metrics are requested for.
    - "time" corresponds to the length of time from the current date that metrics should be retrieved for.
    - "groupby" corresponds to which parameter results should be grouped by
    - One parameter from "fname", "lname", "email", and "id" is allowed at a time. (only "fname" and "lname" can be grouped)
        - The "fname", "lname", "email", and "id" parameters may have a single or multiple values separated by commas.
        - If "fname" and "lname" are given simultaneously as parameters, only one value each is permitted.
    - "county", "time", and "groupby" can be used in any combination
        - One value is permitted for each parameter.
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Metrics Data": [
                {
                "Date Created": String,
                "Appointments Complex Medicaid": Integer,
                "Referred SHOP": Integer,
                "Filed Exemptions": Integer,
                "Enrolled SHOP": Integer,
                "Appointments Held": Integer,
                "Hardship or Difficulty": String,
                "Appointments Post-Enrollment Assistance": Integer,
                "County": String,
                "Trends": String,
                "Appointments Complex Market": Integer,
                "Outreach and Stakeholder Activities": String,
                "Referred Medicaid or CHIP": Integer,
                "Applied Medicaid": Integer,
                "Staff Member ID": Integer,
                "Submission Date": String,
                "Received Education": Integer,
                "Received Post-Enrollment Support": Integer,
                "Appointments Over 3 Hours": Integer,
                "Confirmation Calls": Integer,
                "Appointments Over Hour": Integer,
                "Success Story": String,
                "Selected QHP": Integer,
                "Comments": String,
                "Appointments Scheduled": Integer
                },
                ...,
                ...,
                ...,
                ],
                "Staff Information": {
                "Database ID": Integer,
                "First Name": String,
                "County": String,
                "Type": String,
                "Last Name": String,
                "Email": String
                }
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- If staff members are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If staff members are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license
