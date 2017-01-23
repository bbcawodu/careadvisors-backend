## Patient Assist Scheduler Backend API
    
### Google Calendar API OAuth2 Credentials Authorization Page for Navigators
# NAVIGATORS MUST NOT CHANGE THE NAME OF THE PATIENT INNOVATION CENTER CONSUMER APPOINTMENT GOOGLE CALENDAR. IF THEY DO, THEY WILL NO LONGER BE SCHEDULED APPOINTMENTS
- To retrieve and update Google Calendar API OAuth2 Credentials for a navigator and store it in the database, submit a GET request to http://picbackend.herokuapp.com/v2/calendar_auth/ with the following MANDATORY parameter: "navid".
    - "navid" corresponds to navigator database id.
        - passing a database id that does not appear in the database will result in an error.
        
- If there are no valid credentials for the given navigator id stored in the database, navigator will be redirected to a Google authorization page where they can authorize our application to view and modify their calendar.
- Once the navigator has succesfuly authorized our application or if there are any errors, navigator will be redirected to a page of the following format:
- The response will be a JSON document with the following format:
    ```
    {
        "Data": "Authorized!" (Only if there are authorized navigator credentials in database),
        "Status": {
            "Version": 2.0,
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
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.
    
    
### Available Navigator Appointments API (IN TEST)
#### (Need to add number of available navigators for various time slots)
#### ALL DATES AND TIMES ARE UTC

To retrieve available navigator appointments for a given dictionary of consumer preferences, submit a POST request to: http://picbackend.herokuapp.com/v2/patient_assist_apt_mgr/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

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
            "Version": 2.0,
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
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### View Scheduled Consumer Appointments API (IN TEST)
#### ALL DATES AND TIMES ARE UTC

To retrieve scheduled consumer appointments for a given navigator, submit a GET request to: http://picbackend.herokuapp.com/v2/patient_assist_apt_mgr/ with the following MANDATORY parameter: "navid"

- "navid" must be a base 10 integer

- The response will be a JSON document with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array,
            "Data": {
                        "Scheduled Appointments" :[
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00'(All Appointments are 30 Minutes Long),
                                                            "Appointment Summary" : "alihihifhsjkdhfjkdsfhkjsdf",
                                                        },
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00'(All Appointments are 30 Minutes Long),
                                                            "Appointment Summary" : "alihihifhsjkdhfjkdsfhkjsdf",
                                                        },
                                                        {
                                                            "Navigator Name" : "Bradley Awodu",
                                                            "Navigator Database ID" : 1,
                                                            "Appointment Date and Time" : '2016-12-22T10:00:00'(All Appointments are 30 Minutes Long),
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
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### Add Consumer Appointment with Navigator API (IN TEST)
#### ALL DATES AND TIMES ARE UTC

To add a phone appointment for a consumer with a navigator, submit a PUT request to: http://picbackend.herokuapp.com/v2/patient_assist_apt_mgr/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"Navigator ID": Integer,
"Appointment Date and Time" : '2016-12-22T10:00:00',
"Consumer Info": {
                    "First Name": String,
                    "Middle Name": String (Can be empty),
                    "Last Name": String,
                    "Email": String (Can be empty),
                    "Phone Number": String,
                    "Household Size": Integer,
                    "Plan": String (Can be empty),
                    "Preferred Language": String (Can be empty),
                    
                    Address(Every field within address can be given as an empty string. Address will only be recorded/updated iff a full address is given)
                    "Address Line 1": String (Can be empty),
                    "Address Line 2": String (Can be empty),
                    "City": String (Can be empty),
                    "State": String (Can be empty),
                    "Zipcode": String (Can be empty),
                 }
 
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array,
            "Data": {
                        "Confirmed Appointment" :{
                                                     "Navigator Name" : "Bradley Awodu",
                                                     "Navigator Database ID" : 1,
                                                     "Appointment Date and Time" : '2016-12-22T10:00:00'(All Appointments are 30 Minutes Long),
                                                     "Appointment Title" : "Navigator (Bradley Awodu) appointment with calkfndy pophgfthcdfgcgh",
                                                     "Appointment Summary" : "Consumer will be expecting a call at 2813308004
                                                                              Other Consumer Info:
                                                                              First Name: calkfndy
                                                                              Last Name: pophgfthcdfgcgh
                                                                              Email: kjashkjhd@kjashf.com",
                                                 },
                        "Consumer ID" : Integer,
                    },
           }
}
```

- Data will be a dictionary with the following keys
    - "Confirmed Appointment"
        - Contains info for for the scheduled consumer appointment with navigator
    - "Consumer ID"
        - Database id of the consumer that the appointment was scheduled for
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
    
### Delete Consumer Appointment with Navigator API (IN TEST)
#### ALL DATES AND TIMES ARE UTC

To delete a phone appointment for a consumer with a navigator, submit a DELETE request to: http://picbackend.herokuapp.com/v2/patient_assist_apt_mgr/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"Navigator ID": Integer,
"Appointment Date and Time" : '2016-12-22T10:00:00',
 
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array,
            "Data": {
                        "Deleted" : Boolean
                    },
           }
}
```

- Data will be a dictionary with the following keys
    - "Deleted" will be a boolean declaring whether or not appointment was deleted
    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.