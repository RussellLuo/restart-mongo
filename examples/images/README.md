# Images

An example showing how to manage files as a REST resource based on RESTArt-Mongo.


## Usage

### 1. Start the MongoDB server

```
$ mongod
```

### 2. Run the API

```
$ cd examples/images
$ restart api:api
Directory `/tmp/tmpuEsOMQ` is created for storing uploaded files. Remember to remove it by hand:-)
 * Running on http://127.0.0.1:5000/
```

### 3. Consume the API

1. GET /images

    ```
    $ curl -i http://127.0.0.1:5000/images
    HTTP/1.0 200 OK
    Content-Type: application/json
    X-Pagination-Info: page=1, per-page=10, count=0
    Content-Length: 2
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Sun, 23 Aug 2015 09:04:26 GMT

    []
    ```

2. POST /images

    ```
    $ curl -i -F image=@/tmp/test.jpg http://127.0.0.1:5000/images
    HTTP/1.1 100 Continue

    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Location: http://127.0.0.1:5000/images/55d98d0b6834074d46ad683b
    Content-Length: 35
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Sun, 23 Aug 2015 09:06:19 GMT

    {"_id": "55d98d0b6834074d46ad683b"}
    ```

3. GET /images/pk

    ```
    $ curl -i http://127.0.0.1:5000/images/55d98d0b6834074d46ad683b
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 173
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Sun, 23 Aug 2015 09:07:47 GMT

    {"initial_name": "test.jpg", "_id": "55d98d0b6834074d46ad683b", "date_uploaded": "2015-08-23T09:06:19Z", "storage_path": "20150823/ea51a73c-3de9-4533-8e85-55077b698bb2.jpg"}
    ```

4. PUT /images/pk

    ```
    $ curl -i -X PUT -F image=@/tmp/test.png http://127.0.0.1:5000/images/55d98d0b6834074d46ad683b
    HTTP/1.1 100 Continue

    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Sun, 23 Aug 2015 09:12:54 GMT

    ```

5. PATCH /images/pk

    ```
    $ curl -i -X PATCH http://127.0.0.1:5000/images/55d98d0b6834074d46ad683b
    HTTP/1.0 405 METHOD NOT ALLOWED
    Content-Type: application/json
    Content-Length: 63
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Sun, 23 Aug 2015 09:14:36 GMT

    {"message": "The method is not allowed for the requested URL."}
    ```

6. DELETE /images/pk

    ```
    $ curl -i -X DELETE http://127.0.0.1:5000/images/55d98d0b6834074d46ad683b
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Sun, 23 Aug 2015 09:15:43 GMT

    ```
