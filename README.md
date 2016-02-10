# Metrics Backend

This is the code for the backend component of our metrics and appointments apps.
It enables the API that transmits data between the frontend and the backend.

## Installation

This app uses a django installation hosted on Heroku. To install, go to:
https://devcenter.heroku.com/articles/getting-started-with-python#introduction and follow the instructions
for your particular operating system.

## Usage

To add an appointment to the database using our appointments API, submit a POST request to:
obscure-harbor-6074.herokuapp.com/submitappointment/. The POST data should be a JSON document which has the following
format:
```
{"First Name": String,
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
