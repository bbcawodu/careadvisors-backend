## Presence Healthcare Appointment Scheduler Backend

### Presence Healthcare Appointment Addition API
To add an appointment to the database using our appointments API, make a POST request to: http://picbackend.herokuapp.com/submitappointment/. The POST data should be a JSON document which has the following format:

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
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
           }
}
```

- If there are no errors in the JSON Body doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "Status" dictionary.
    - An instance of the Appointment class corresponding to the JSON Body doc will be created and saved in the database.
        - If there isn't a consumer database entry with an email field corresponding to the POST, one is created.
        - If there isn't a location database entry with a name field corresponding to the POST, one is created.
        - If there isn't a staff database entry with an email field corresponding to the POST, one is created.
    
- If there are errors in the JSON Body doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        - Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.



### Presence Healthcare Appointments Viewer
Go to http://picbackend.herokuapp.com/viewappointments to view what appointments have been submitted by consumers and to whom they have been assigned.