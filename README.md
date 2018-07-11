# Community Connect Backend Server

This is the code for the backend server for Community Connect related apps. It enables the API that transmits data between the frontend and the backend servers of community connect related applications.



## Installation

This is a Django application that is hosted on Heroku. To install Heroku CLI for easier code editing and deployment, go to: [Django Deployment on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) and follow the instructions for your particular operating system.



## Community Connect Backend Library API Documentation

[API Version 2](docs/API_Version_2/README.md) (CURRENT VERSION)


## Chicago Public Schools Backend Documentation

[Chicago Public Schools Backend Documentation](docs/chicago_public_schools/README.md) (CURRENT VERSION)


## Writing and Running Tests README

[Writing and Running Tests README](docs/Testing.md)
    
    
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


## CODING NOTES
- Use len instead of .count in methods that iterate over that same queryset since the results will be cached and it is preferable to use len in that case since this avoids hitting the the database again, and also the possibly of retrieving a different number of results'

