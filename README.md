# Metrics Backend

This is the code for the backend component of our metrics and appointments apps.
It enables the API that transmits data between the frontend and the backend.

## Installation

This app runs on a django installation hosted on Heroku. To install Heroku for code editing, go to:
https://devcenter.heroku.com/articles/getting-started-with-python#introduction and follow the instructions
for your particular operating system.

## Usage

##Presence Healthcare Appointment Scheduler Backend
To add an appointment to the database using our appointments API, submit a POST request to:
http://obscure-harbor-6074.herokuapp.com/submitappointment/. The POST data should be a JSON document which has the
following format:
```
{
 "First Name": String,
 "Last Name": String,
 "Email": String,
 "Phone Number": String,
 "Preferred Language": String,
 "Best Contact Time": String,
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
If there are no errors in the POSTed JSON doc:
- "Error Code" will be 0.
- There will be no "Errors" key in the "status" dictionary.
- An instance of the Appointment class corresponding to the POSTed JSON doc will be created and saved in the database.
    - If there isn't a consumer database entry with an email field corresponding to the POST, one is created.
    - If there isn't a location database entry with a name field corresponding to the POST, one is created.
    
If there are errors in the POSTed JSON doc:
-"Error Code" will be 1.
- An array of length > 0 will be the value for the "Errors" key in the "status" dictionary.
    -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
- No changes are made to the database.


## Metrics Backend

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
