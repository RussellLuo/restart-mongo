# CSV

Some examples showing how to handle CSVs based on `RESTArt-Mongo`.


## Prerequisites

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


## Examples

1. [Student](student)
2. [Generic-CSV](generic_csv)
