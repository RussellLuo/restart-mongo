# User

An example showing how to make the MongoDB collections to be REST resources based on RESTArt-Mongo.


## Usage

### 1. Start the MongoDB server

```
$ mongod
```

### 2. Run the API

```
$ cd examples/user
$ restart user:api
 * Running on http://127.0.0.1:5000/
```

### 3. Consume the API

1. GET /users

    ```
    $ curl -i http://127.0.0.1:5000/users
    HTTP/1.0 200 OK
    Content-Type: application/json
    X-Pagination-Info: page=1, per-page=10, count=0
    Content-Length: 2
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 14 Aug 2015 00:17:31 GMT

    []
    ```

2. POST /users

    ```
    $ curl -i -H "Content-Type: application/json" -d '{
        "name": "russell",
        "password": "123456",
        "date_joined": "datetime(2015-08-14T00:00:00Z)"
    }' http://127.0.0.1:5000/users
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 35
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 14 Aug 2015 00:19:51 GMT

    {"_id": "55cd34276834073adc4a8170"}
    ```

3. GET /users/<pk>

    ```
    $ curl -i http://127.0.0.1:5000/users/55cd34276834073adc4a8170
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 115
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 14 Aug 2015 00:20:59 GMT

    {"password": "123456", "_id": "55cd34276834073adc4a8170", "name": "russell", "date_joined": "2015-08-14T00:00:00Z"}
    ```

4. PUT /users/<pk>

    ```
    $ curl -i -X PUT -H "Content-Type: application/json" -d '{
        "name": "tracey",
        "password": "123456",
        "date_joined": "datetime(2015-08-14T00:00:00Z)"
    }' http://127.0.0.1:5000/users/55cd34276834073adc4a8170
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 14 Aug 2015 00:22:07 GMT

    ```

5. PATCH /users/<pk>

Please refer to [RFC 6902][1] for the exact JSON Patch syntax.

```
$ curl -i -X PATCH -H "Content-Type: application/json" -d '[{
    "op": "add",
    "path": "/password",
    "value": "666666"
}]' http://127.0.0.1:5000/users/55cd34276834073adc4a8170
HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 0
Server: Werkzeug/0.10.4 Python/2.7.6
Date: Fri, 14 Aug 2015 00:23:47 GMT

```

6. DELETE /users/<pk>

    ```
    curl -i -X DELETE http://127.0.0.1:5000/users/55cd34276834073adc4a8170
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 14 Aug 2015 00:24:52 GMT

    ```


[1]: http://tools.ietf.org/html/rfc6902
