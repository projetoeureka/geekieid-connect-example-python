# geekieid-connect-example-python

This is a Python example of an OAuth 2.0 integration with GeekieID
Connect.

You can see this example running live at
https://geekieid-connect-ex-python.herokuapp.com/.

## Running the example

To run this locally, you can request a local development **client_id**
(you'll have to specify the exact **redirect_uri** for local
development, including the port), then edit the value of
`OAUTH_CLIENT_ID` at the top of [app.py][apppy] and then run the program
with

    gunicorn -w 4 -b 127.0.0.1:3000 --preload app:app

For the above example, the value of **redirect_uri** should be
`http://localhost:3000/oauthcallback`.

## Deploying the example

To be able to see this in action in a live remote server, this project
is designed to be ready to be deployed to Heroku. Adjust the value of
`OAUTH_CLIENT_ID` at the top of [app.py][apppy] to a **client_id**
that's registered to the correct **redirect_uri** and then just push
this repository to Heroku:

    git push git@heroku.com:<your project>.git master

For the above example, the value of **redirect_uri** should be
`https://<your project>.herokuapp.com/oauthcallback`.

[apppy]: https://github.com/projetoeureka/geekieid-connect-example-python/blob/master/app.py#L10
