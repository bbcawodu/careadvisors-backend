## Staff Account Backend API

### Staff Data Submission API
To modify or add members of the PICStaff class in the database, submit a POST request to: http://picbackend.herokuapp.com/editstaff/. The POST data a JSON document using the following template:

```
{
"First Name": String,
"Last Name": String,
"Email": String,
"User Type": String,
"User County": String,
"Base Location Names": [Strings (Can be None or empty string)], # If any locations are not found, an error will be added and the staff member will still be saved
"MPN": String(Can be None or empty string),
"Database ID": Integer(Required when "Database Action" == "Staff Modification" or "Staff Deletion"),
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
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Staff Data Retrieval API
- To retrieve staff data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/staff? with the following optional parameters: "fname", "lname", "email", "mpn", "id"
    - "fname" corresponds to first name.
    - "lname" corresponds to last name.
    - "email" corresponds to email.
    - "mpn" corresponds to mpn.
    - "county" corresponds to email.
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
                "Region": String,
                "First Name": String,
                "Last Name": String,
                "Authorized Credentials": Boolean,
                "Base Location": [{
                                    "Location Name": String,
                                    "Address Line 1": String,
                                    "Address Line 2": String,
                                    "City": String,
                                    "State": String,
                                    "Zipcode": String,
                                    "Country": String,
                                    "Database Action": String
                                 },
                                  ...(Can be Empty)],
                "MPN": String,
                "Consumers":[
                                {
                                "First Name": String,
                                "Best Contact Time": String,
                                "Database ID": Integer,
                                "Last Name": String,
                                "Preferred Language": String,
                                "Navigator": String,
                                "Phone Number": String,
                                "Email": String
                                },
                                ....
                            ],
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
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.
    
    
### Google Calendar API OAuth2 Credentials Authorization Page for Navigators
# NAVIGATORS MUST NOT CHANGE THE NAME OF THE PATIENT INNOVATION CENTER CONSUMER APPOINTMENT GOOGLE CALENDAR. IF THEY DO, THEY WILL NO LONGER BE SCHEDULED APPOINTMENTS
- To retrieve and update Google Calendar API OAuth2 Credentials for a navigator and store it in the database, submit a GET request to http://picbackend.herokuapp.com/v1/calendar_auth/? with the following MANDATORY parameter: "navid".
    - "navid" corresponds to navigator database id.
        - passing a database id that does not appear in the database will result in an error.
        
- If there are no valid credentials for the given navigator id stored in the database, navigator will be redirected to a Google authorization page where they can authorize our application to view and modify their calendar.
- Once the navigator has succesfuly authorized our application or if there are any errors, navigator will be redirected to a page of the following format:
- The response will be a JSON document with the following format:
    ```
    {
        "Data": "Authorized!" (Only if there is authorized navigator credentials in database),
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
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.
    
    
### Available Navigator Appointments API (IN TEST)
#### ALL DATES AND TIMES ARE UTC

To retrieve available navigator appointments for a given dictionary of consumer preferences, submit a POST request to: http://picbackend.herokuapp.com/v1/getnavappointments/. The POST data a JSON document using the following template:

```
{
"Preferred Times": ['2016-12-22T10:00:00'(Preferred Time must be a string iso formatted date and time),
                    '2016-12-22T14:00:00'(Preferred Time must be a string iso formatted date and time),
                    '2016-12-22T17:00:00'(Preferred Time must be a string iso formatted date and time),
                    ...
                    ] (List of date times to request navigator appointments for MUST BE IN UTC)(Can be an Empty List),
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array,
            "Data": {
                        "Next Available Appointments" :[
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                        },
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                        },
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                        },
                                                        ...
                                                        ],
                        "Preferred Appointments" : [
                                                        [
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            ...
                                                        ](Can Be Empty),
                                                        [
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            ...
                                                        ](Can Be Empty),
                                                        [
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Schedule Appointment Link" : "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid=1",
                                                            },
                                                            ...
                                                        ](Can Be Empty),
                                                        ...
                                                   ] (Can Be Empty),
                    },
           }
}
```

- Data will be a dictionary with the following keys
    - "Next Available Appointments"
        - Will be empty if "Preferred Times" has at least one valid time
        - An array of available appointments with navigators starting from the time the request was made
    - "Preferred Appointments"
        - Will be empty if "Preferred Times" is empty
        - An array of arrays of available appointments with navigators
        - Length of "Preferred Appointments" will EXACTLY match the length of the "Preferred Times" array in the request
        - Array of navigator appointments at the index of the "Preferred Appointments" array corresponds to the  date and time at the same index of the "Preferred Times" array
            - If no navigator appointments are found for the date and time at a given index of preferred times, the array of navigator appointments at that index of "Preferred Appointments" will be empty
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
    
### View Scheduled Consumer Appointments API (IN TEST)
#### ALL DATES AND TIMES ARE UTC

To retrieve scheduled consumer appointments for a given navigator, submit a GET request to: http://picbackend.herokuapp.com/v1/viewscheduledappointments/? with the following MANDATORY parameter: "navid"

- The response will be a JSON document with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array,
            "Data": {
                        "Scheduled Appointments" :[
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Appointment Summary" : "alihihifhsjkdhfjkdsfhkjsdf",
                                                        },
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Appointment Summary" : "alihihifhsjkdhfjkdsfhkjsdf",
                                                        },
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00',
                                                            "Appointment Summary" : "alihihifhsjkdhfjkdsfhkjsdf",
                                                        },
                                                        ...
                                                  ](In chronological order)
           }
}
```

- Data will be a dictionary with the following keys
    - "Scheduled Appointments"
        - An array of scheduled consumer appointments.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.