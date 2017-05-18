## Ranked Specific Concerns Backend API (IN DEVELOPMENT)

### Ranked Specific Concerns Retrieval API
To retrieve a ranked list of ConsumerSpecificConcern class entries based on a submitted ranked list of consumer general
concerns that exist in our db, submit a POST request to: http://picbackend.herokuapp.com/v2/ranked_specific_concerns/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document using the following template:

```
{
"ranked_general_concerns": [
                                String,
                                ...,
                                ...
                            ] (Must contain at least one entry)(Order matters.)(NO DUPLICATES),
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": 2.0,
            "Errors": Array,
            "Warnings": Array,
           },
 "Data": [
                {
                "question": String,
                "related_general_concerns": [
                                                {
                                                    "name": String,
                                                    "Database ID": Integer
                                                },
                                                ...,
                                                ...
                                             ] or Null,
                "Database ID": Integer,
            },
            {
                "question": String,
                "related_general_concerns": [
                                                {
                                                    "name": String,
                                                    "Database ID": Integer
                                                },
                                                ...,
                                                ...
                                             ] or Null,
                "Database ID": Integer,
            },
            {
                "question": String,
                "related_general_concerns": [
                                                {
                                                    "name": String,
                                                    "Database ID": Integer
                                                },
                                                ...,
                                                ...
                                             ] or Null,
                "Database ID": Integer,
            },
            ...,
            ...
         ](Up to 10 entries)(In order of non-increasing relevance),
}
```

    
- If there are errors in the JSON Body document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No data will be returned.