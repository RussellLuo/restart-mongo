# CSV

An example showing how to render MongoDB collection data into CSV.


## Usage

### 1. Start the MongoDB server

```
$ mongod
```

### 2. Prepare some data

```
$ mongo
> use test
> db.student.insert({name: 'russell', course: 'physics', score: 90})
> db.student.insert({name: 'tracey', course: 'economics', score: 92})
```

### 3. Run the API

```
$ cd examples/csv
$ restart student:api
 * Running on http://127.0.0.1:5000/
```

### 4. Consume the API

1. GET /students

    ```
    $ curl -i http://127.0.0.1:5000/students
    HTTP/1.0 200 OK
    Content-Type: application/json
    X-Pagination-Info: page=1, per-page=10, count=2
    Content-Length: 185
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 28 Aug 2015 13:33:42 GMT

    [{"course": "physics", "_id": "55e060d6a48f94e293270acd", "name": "russell", "score": 90.0}, {"course": "economics", "_id": "55e060dfa48f94e293270ace", "name": "tracey", "score": 92.0}]
    ```

2. GET /students.csv

    ```
    curl -i http://127.0.0.1:5000/students.csv
    HTTP/1.0 200 OK
    Content-Type: text/csv
    X-Pagination-Info: page=1, per-page=10, count=2
    Content-Length: 67
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 28 Aug 2015 13:34:31 GMT

    姓名,科目,成绩
    russell,physics,90.0
    tracey,economics,92.0
    ```

3. GET /students/pk

    ```
    curl -i http://127.0.0.1:5000/students/55e060dfa48f94e293270ace
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 91
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 28 Aug 2015 13:35:27 GMT

    {"course": "economics", "_id": "55e060dfa48f94e293270ace", "name": "tracey", "score": 92.0}
    ```

4. GET /students/pk.csv

    ```
    curl -i http://127.0.0.1:5000/students/55e060dfa48f94e293270ace.csv
    HTTP/1.0 200 OK
    Content-Type: text/csv
    Content-Length: 45
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Fri, 28 Aug 2015 13:36:15 GMT

    姓名,科目,成绩
    tracey,economics,92.0
    ```
