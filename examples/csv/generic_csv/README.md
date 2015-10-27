# Generic-CSV

An example showing how to implement a generic resource that can export different databases and collections into CSVs.


## Usage

### 1. Run the API

```
$ cd examples/csv/generic-csv
$ restart api:api
 * Running on http://127.0.0.1:5000/
```

### 2. Consume the API

1. GET /generic-csvs.csv?database=test&collection_name=student&fields=name,course,score

    ```
    $ curl -i http://127.0.0.1:5000/generic-csvs.csv?database=test&collection_name=student&fields=name,course,score
    HTTP/1.0 200 OK
    Content-Type: text/csv
    X-Pagination-Info: page=1, per-page=10, count=2
    Content-Length: 64
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Mon, 26 Oct 2015 15:05:29 GMT

    name,course,score
    russell,physics,90.0
    tracey,economics,92.0
    ```
