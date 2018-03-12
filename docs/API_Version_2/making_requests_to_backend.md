# Making Requests to Backend Server Endpoints README
#### NOTE: All requests to backend endpoints must be made through AJAX(Request header must include key:value, "X-Requested-With":"XMLHttpRequest"). You will receive a 403 Forbidden error code if you make a request through any other method.

## GET Endpoints
All GET endpoints make no change to the database state.
- All GET endpoints that have a corresponding POST, PUT, or DELETE endpoint will have a "csrftoken:[value]" pair embedded
in the cookies. This token value is required to be present the header of any request to the corresponding POST, PUT, or DELETE
enpoint in the form of "X-CSRFToken:[value]". The POST, PUT, or DELETE request will be rejected otherwise. These tokens
are refreshed every ~1 hour, so it is essential to keep the token refreshed at a smaller interval.

## POST, PUT, and DELETE Endpoints
POST, PUT, and DELETE endpoints may make changes to the database state.
- All requests to POST, PUT, or DELETE enpoints must have a token embedded in the header of the request in the form of
"X-CSRFToken:[value]". The POST, PUT, or DELETE request will be rejected otherwise. This token is obtained by making a
request to the corresponding GET endpoint and retrieving the token from the response. The token is present in the cookies
of the response in the form of "csrftoken:[value]".These tokens are refreshed every ~1 hour, so it is essential to
retrieve the token at a smaller interval.
