## Call to Action API

### Call to Action Management API
- To create/update the Call to Action for a given intent keyword, make a GET request to http://picbackend.herokuapp.com/v2/cta_management/
  with the following optional parameter: "intent".
    - If intent keyword is present in the request, the current image will be shown for the given intent keyword if there
      is an entry for it in the db. If there is no intent entry in the db, a blank form will be shown.
    - if no intent keyword is present in the request, a blank form will be shown.
    - All keywords are unique in the db. If chosen keyword already has an entry in the db, the old entry will be updated.
    
### Call to Action Retrieval API
- To retrieve information for a call to action that is stored in the backend, submit a GET request to
  http://picbackend.herokuapp.com/v2/cta/ with the following mandatory parameter: "intent"
    - Results will be filtered by the given parameters.
    - "intent" corresponds to the intent keyword for the Call to action that you want to retrieve.
        - Must be a string
        - Use keyword 'all' to retrieve all call to actions in db
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Intent": String,
                "Picture": String(URL),
                "Database ID": Integer,
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

- If a call to action is found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If a call to action is not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.