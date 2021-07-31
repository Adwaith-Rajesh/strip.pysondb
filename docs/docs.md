# Adding values to the DB

## DB.add

- #### `DB.add(data: dict[str, Any]) -> str`
- The `add` methods accepts the data to be inserted as the first argument and returns the `id` for the insertion.

```python
from pysondb import DB

db = DB("test.json")
_id = db.add({
    "name": "ad",
    "age": 3
})
print(_id)
print(db)
```

    6273619734359589
    {'6273619734359589': {'name': 'ad', 'age': 3}}

```commandline
cat test.json
```

    {
        "6273619734359589": {
            "name": "ad",
            "age": 3
        }
    }

## DB.add_many

- `DB.add_many(data: list[dict[str, Any]) -> None`
- The `add_many` methods accepts a list of all the data need to inserted. It does not return anything.

```python
from pysondb import DB

db = DB("test.json")
db.add_many(
    [
        {"name": "name1", "age": 1},
        {"name": "name2", "age": 2},
        {"name": "name3", "age": 3},
    ]
)
print(db)
```

    {'1725641998589765': {'name': 'name1', 'age': 1},
     '1392420245559002': {'name': 'name2', 'age': 2},
     '2080111934769372': {'name': 'name3', 'age': 3}}

```commandline
cat test.json
```

    {
        "1725641998589765": {
            "name": "name1",
            "age": 1
        },
        "1392420245559002": {
            "name": "name2",
            "age": 2
        },
        "2080111934769372": {
            "name": "name3",
            "age": 3
        }
    }

# Getting values from the DB

## DB.get_all

- `DB.get_all() -> dict[str, dict[str, Any]]`
- The `get_all` methods return a the entire the DB as is.

```python
from pysondb import DB

db = DB("test.json")
db.add_many(
    [
        {"name": "name1", "age": 1},
        {"name": "name2", "age": 2},
        {"name": "name3", "age": 3},
        {"name": "name4", "age": 4}
    ]
)
print(db.get_all())
```

    {'9566428341785923': {'name': 'name1', 'age': 1}, '2622334761063704': {'name': 'name2', 'age': 2}, '9498894010130491': {'name': 'name3', 'age': 3}, '2434460879836141': {'name': 'name4', 'age': 4}}

## DB.get_by_id

- `DB.get_by_id(_id: str) -> None | dict[str, Any]`
- The `get_by_id` method takes in the `id` of the reocrd to get as a `string` and returns the corresponding record.

```python
from pysondb import DB

db = DB("test.json")
id1 = db.add({"name": "name1", "age": 1})
id2 = db.add({"name": "name1", "age": 1})

print(db)

print(db.get_by_id(id1))

```

    {'4758743790353209': {'name': 'name1', 'age': 1},
     '1223706652062184': {'name': 'name1', 'age': 1}}
    {'name': 'name1', 'age': 1}

## DB.get_by_query

- `DB.get_by_query(query: dict[str, Any]) -> dict[str, dict[str, Any]]`
- The `get_by_query` method takes the query as a `dict`, and returns all the records that satisfy all the query conditions.

```python
from pysondb import DB

db = DB("test.json")

db.add_many(
    [
        {"name": "name1", "age": 1, "place": "canada"},
        {"name": "name2", "age": 2, "place": "texas"},
        {"name": "name3", "age": 3, "place": "denmark"},
        {"name": "name1", "age": 4, "place": "texas"}
    ]
)

print(db.get_by_query({"place": "texas"}))

print(db.get_by_query({"name": "name1", "place": "canada"}))
```

    {'3169757142289922': {'name': 'name2', 'age': 2, 'place': 'texas'}, '1633864560323871': {'name': 'name1', 'age': 4, 'place': 'texas'}}

    {'2000750416342679': {'name': 'name1', 'age': 1, 'place': 'canada'}}

# Updating values

## DB.update_by_id

- `DB.update_by_id(_id: str, data: dict[str, Any]) -> None`
- The `update_by_id` method takes the `id` of the record to update the values

```python
from pysondb import DB

db = DB("test.json")

id1 = db.add({"name": "name1", "age": 3})
id2 = db.add({"name": "name2", "age": 4})

print(db)

db.update_by_id(id1, {"name": "Changed"})
print(db)
```

    {'3171129260736336': {'name': 'name1', 'age': 3},
     '2076036970160909': {'name': 'name2', 'age': 4}}

    {'3171129260736336': {'name': 'Changed', 'age': 3},
     '2076036970160909': {'name': 'name2', 'age': 4}}

## DB.update_by_query

- `DB.update_by_query(query: dict[str, Any], data: dict[str, Any]) -> list[str]`
- The `update_by_query` takes in the query as the first argument and the data to update as the second. It returns a list of id's of all the values it updated.

```python
from pysondb import DB

db = DB("test.json")

db.add_many(
    [
        {"name": "name1", "age": 1, "place": "canada"},
        {"name": "name2", "age": 2, "place": "texas"},
        {"name": "name3", "age": 3, "place": "denmark"},
        {"name": "name1", "age": 4, "place": "texas"}
    ]
)

print(db)

ids = db.update_by_query({"name": "name1", "place": "canada"}, {"age": 69})
print(ids)
print(db)
```

    {'2003334936182502': {'name': 'name1', 'age': 1, 'place': 'canada'},
     '2534038326021519': {'name': 'name2', 'age': 2, 'place': 'texas'},
     '2659937557555512': {'name': 'name3', 'age': 3, 'place': 'denmark'},
     '1404449036366188': {'name': 'name1', 'age': 4, 'place': 'texas'}}

    ['2003334936182502']
    {'2003334936182502': {'name': 'name1', 'age': 69, 'place': 'canada'},
     '2534038326021519': {'name': 'name2', 'age': 2, 'place': 'texas'},
     '2659937557555512': {'name': 'name3', 'age': 3, 'place': 'denmark'},
     '1404449036366188': {'name': 'name1', 'age': 4, 'place': 'texas'}}

# Deleting values from the DB

## DB.delete_by_id

- `DB.delete_by_id(_id: str) -> None`
- The `delete_by_id` takes in the `id` of the record to delete.

```python
from pysondb import DB

db = DB("test.json")
id1 = db.add({"name": "ad", "age": 16})
id2 = db.add({"name": "ad2", "age": 34})

print(db)

db.delete_by_id(id1)
print(db)
```

    {'2858848216450110': {'name': 'ad', 'age': 16},
     '2613659147900249': {'name': 'ad2', 'age': 34}}

    {'2613659147900249': {'name': 'ad2', 'age': 34}}

## DB.delete_by_query

- `DB.delete_by_query(query: dict[str, Any]) -> list[str]`
- The `delete_by_query` accepts the query as the first argument and deletes all the record that satisfy all the condition in the query and returns as list of id's of all the values it deleted.

```python
from pysondb import DB

db = DB("test.json")

db.add_many(
    [
        {"name": "name1", "age": 1, "place": "canada"},
        {"name": "name2", "age": 2, "place": "texas"},
        {"name": "name3", "age": 3, "place": "denmark"},
        {"name": "name1", "age": 4, "place": "texas"}
    ]
)

print(db)

ids = db.delete_by_query({"name": "name1"})
print(ids)
print(db)
```

    {'3229138297315205': {'name': 'name1', 'age': 1, 'place': 'canada'},
     '9823554215816330': {'name': 'name2', 'age': 2, 'place': 'texas'},
     '2038522309502333': {'name': 'name3', 'age': 3, 'place': 'denmark'},
     '2377812238787017': {'name': 'name1', 'age': 4, 'place': 'texas'}}

    ['3229138297315205', '2377812238787017']
    {'9823554215816330': {'name': 'name2', 'age': 2, 'place': 'texas'},
     '2038522309502333': {'name': 'name3', 'age': 3, 'place': 'denmark'}}

## DB.delete_all

- `DB.delete_all() -> None`
- The `delete_all` methods deletes all the values from the DB

```python
from pysondb import DB

db = DB("test.json")

db.add_many(
    [
        {"name": "name1", "age": 1, "place": "canada"},
        {"name": "name2", "age": 2, "place": "texas"},
        {"name": "name3", "age": 3, "place": "denmark"},
        {"name": "name1", "age": 4, "place": "texas"}
    ]
)

print(db)

db.delete_all()
print(db)
```

    {'1108028485915772': {'name': 'name1', 'age': 1, 'place': 'canada'},
     '2425696502050419': {'name': 'name2', 'age': 2, 'place': 'texas'},
     '2508040636802095': {'name': 'name3', 'age': 3, 'place': 'denmark'},
     '7667106027499809': {'name': 'name1', 'age': 4, 'place': 'texas'}}

    {}

# Extras

## Creating an in memory DB

```python
from pysondb import DB

db = DB("test.json", in_memory=True)  # This will not store any of the data or the changes in a file
```

## DB.force_save

- When the DB is an in memory DB, the changes are not saved to a file. If you want to save them to a file then use `DB.force_save`

```python
from pysondb import DB

db = DB("test.json", in_memory=True)
db.add({"name": "test", "age": 2})  # This will not cause any change in the "test.json" file

# To save the changes in ".json" file use
db.force_save()
```

---
