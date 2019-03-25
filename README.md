Rebay is a fully secure online store API that has three resources:

1) Items, which are things that are for sale in the store.
2) Stores, which are the stores that sell the particular item.
3) Users, which need to be logged in in order to manipulate any of the data.

Rebay was built using Flask in Python and PostgreSQL for the SQL database engine.
JWT was used to set up authentication processes and privileged users. Anyone
accessing the API is able to view data, but users must be logged in in order
to manipulate any of the data with the exception of the user resource. Any accessing the site will be able to register with the /register route. Once logged
in users will be able to create items and stores, as well as manipulate
corresponding data.

Due to the time constraints I did not have time to put together a front end store   
So I focused on the backend database and structure. Instead, when the user visits
the live store, they will see a JSON of all the items featured on the website
as well as the prices of those items.

*****RESOURCES AND ROUTES******

Note All requests use JSON format objects.

User Resource:
'/register'  --> Registers a user by passing in a Post request with username and
                    password

'/user/<int:user_id>' ---> GET, DELETE, PUT to user (read, destroy, update)

'/auth'  --> Authenticate user by sending a POST request with username/password

'/logout' --> logs out a user by sending a POST request with username/password

'/refresh' --> Refreshes JWT by sending POST request. (Must have Refresh Token)

'/recover' --> recovers the password by sending a POST request with Username and new password.

Item Resource:
'/item/<string:name>' --> Allows a user to CRUD an Item.

'/' --> GET request which shows all items in the database

Store Resorse:
'/store/<string:name>'--> GET, DELETE, PUT to store (read, destroy, update)
                        (update requires JSON with updated value)

'/stores' --> shows all stores
