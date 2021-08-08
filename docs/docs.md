# Adding values to the DB

## `DB.add(data: dict[str, Any]) -> str:`

### The `DB.add` method takes the data to be added as a parameter and returns the `id` of the added data.

```python
from pysondb import DB

db = DB(keys = ["name", "age"])
_id = db.add({
    "name": "ad",
    "age": 3
})

print(_id)
print(db)
```

    86162734114102357614
    {'86162734114102357614': {'name': 'ad', 'age': 3}}

## `DB.add_many(data: list[dict[str, Any]]) -> None`:

### The `DB.add_many` method takes a list of values that needs to be inserted into the DB

```python
from pysondb import DB

db = DB(keys = ["name", "age"])

db.add_many([
    {"name": "ad", "age": 3},
    {"name": "fred", "age": 4}
])

print(db)
```

    {'9591351855895146995': {'name': 'ad', 'age': 3},
     '76989986112571672716': {'name': 'fred', 'age': 4}}

# Getting values from the DB

## `DB.get_by_id(_id: str) -> None | dict[str, Any]:`

### The `DB.get_by_id` method takes in the id you want to access and returns the corresponding value.

```python
from pysondb import DB

db = DB(keys = ["name", "age"])

id1 = db.add({"name": "ad", "age": 2})
id2 = db.add({"name": "fred", "age": 3})

print(db)

print(db.get_by_id(id1))
```

    {'95037114323012551332': {'name': 'ad', 'age': 2},
     '32279388482235947196': {'name': 'fred', 'age': 3}}

    {'name': 'ad', 'age': 2}

## `DB.get_by_query(query: dict[str, Any]) -> dict[str, Dict[str, Any]]:`

### The `DB.get_by_query` method takes in the query as a dict and returns all the values that matches all the condition in the query

```python
from pysondb import DB

db = DB(keys = ["name", "age", "place"])

db.add_many([
    {"name": "ad", "age": 1, "place": "canada"},
    {"name": "fred", "age": 2, "place": "canada"},
    {"name": "dev", "age": 1, "place": "texas"}
])

print(db)

print(db.get_by_query({"age": 1}))

print(db.get_by_query({"place": "canada"}))

print(db.get_by_query({"age": 1, "place": "canada"}))
```

    {'5262598325755300825': {'name': 'ad', 'age': 1, 'place': 'canada'},
     '18020291891207081045': {'name': 'fred', 'age': 2, 'place': 'canada'},
     '77364941558209304711': {'name': 'dev', 'age': 1, 'place': 'texas'}}

    {'5262598325755300825': {'name': 'ad', 'age': 1, 'place': 'canada'}, '77364941558209304711': {'name': 'dev', 'age': 1, 'place': 'texas'}}

    {'5262598325755300825': {'name': 'ad', 'age': 1, 'place': 'canada'}, '18020291891207081045': {'name': 'fred', 'age': 2, 'place': 'canada'}}

    {'5262598325755300825': {'name': 'ad', 'age': 1, 'place': 'canada'}}

## `DB.get_all() -> dict[str, dict[str, Any]]:`

### The `DB.get_all` method returns the entire DB

```python
from pysondb import DB

db = DB(keys = ["name", "age", "place"])

db.add_many([
    {"name": "ad", "age": 1, "place": "canada"},
    {"name": "fred", "age": 2, "place": "canada"},
    {"name": "dev", "age": 1, "place": "texas"}
])

print(db.get_all())
```

    {'96964062534918447921': {'name': 'ad', 'age': 1, 'place': 'canada'}, '58168554184395949908': {'name': 'fred', 'age': 2, 'place': 'canada'}, '75810279465693821328': {'name': 'dev', 'age': 1, 'place': 'texas'}}

## `DB.pop(_id: str) -> dict[str, Any] | None`

### The `DB.pop` methods takes in the `id`, and returns the corresponding values and also deletes it.

```python
from pysondb import DB

db = DB(keys = ["name", "age"])

id1 = db.add({"name": "ad", "age": 2})
id2 = db.add({"name": "fred", "age": 3})

print(db)

val = db.pop(id1)

print(val)

print(db)
```

    {'50644806341738425895': {'name': 'ad', 'age': 2},
     '17298553930722956170': {'name': 'fred', 'age': 3}}

    {'name': 'ad', 'age': 2}

    {'17298553930722956170': {'name': 'fred', 'age': 3}}

# Updating values in the DB

## `DB.update_by_id(_id: str, data: Dict[str, Any]) -> None:`

### The `DB.update_by_id` methods, takes in the `id` of the data to change and the values that needs to updated as a dict

```python
from pysondb import DB

db = DB(keys = ["name", "age"])

id1 = db.add({"name": "ad", "age": 2})
id2 = db.add({"name": "fred", "age": 3})

print(db)

db.update_by_id(id1, {"name": "updated"})
print(db)
```

    {'80858900245023206374': {'name': 'ad', 'age': 2},
     '61477679248224695053': {'name': 'fred', 'age': 3}}

    {'80858900245023206374': {'name': 'updated', 'age': 2},
     '61477679248224695053': {'name': 'fred', 'age': 3}}

## `DB.update_by_query(query: dict[str, Any], data: dict[str, Any]) -> list[str]:`

### The `DB.update_by_query` method takes in the query as the first methods and the data to update as the second, returns the id of all the data that was updated

```python
from pysondb import DB

db = DB(keys = ["name", "age", "place"])

db.add_many([
    {"name": "ad", "age": 1, "place": "canada"},
    {"name": "fred", "age": 2, "place": "canada"},
    {"name": "dev", "age": 1, "place": "texas"}
])

print(db)

ids = db.update_by_query({"age": 1}, {"place": "denmark"})

print(ids)

print(db)
```

    {'83229536472899161051': {'name': 'ad', 'age': 1, 'place': 'canada'},
     '23723621461536992544': {'name': 'fred', 'age': 2, 'place': 'canada'},
     '98959451713674556430': {'name': 'dev', 'age': 1, 'place': 'texas'}}

    ['83229536472899161051', '98959451713674556430']

    {'83229536472899161051': {'name': 'ad', 'age': 1, 'place': 'denmark'},
     '23723621461536992544': {'name': 'fred', 'age': 2, 'place': 'canada'},
     '98959451713674556430': {'name': 'dev', 'age': 1, 'place': 'denmark'}}

# Deleting values from the db

## `DB.delete_by_id(_id: str) -> None:`

```python
from pysondb import DB

db = DB(keys = ["name", "age"])

id1 = db.add({"name": "ad", "age": 2})
id2 = db.add({"name": "fred", "age": 3})

print(db)

db.delete_by_id(id1)

print(db)
```

    {'97648742833309339157': {'name': 'ad', 'age': 2},
     '87621755412163193613': {'name': 'fred', 'age': 3}}

    {'87621755412163193613': {'name': 'fred', 'age': 3}}

## `DB.delete_by_query(query: dict[str, Any]) -> list[str]:`

```python
from pysondb import DB

db = DB(keys = ["name", "age", "place"])

db.add_many([
    {"name": "ad", "age": 1, "place": "canada"},
    {"name": "fred", "age": 2, "place": "canada"},
    {"name": "dev", "age": 1, "place": "texas"}
])

print(db)


ids = db.delete_by_query({"age": 2})
print(ids)

print(db)
```

    {'69967688724871017963': {'name': 'ad', 'age': 1, 'place': 'canada'},
     '46912058793349655586': {'name': 'fred', 'age': 2, 'place': 'canada'},
     '49620712450163338969': {'name': 'dev', 'age': 1, 'place': 'texas'}}

    ['46912058793349655586']

    {'69967688724871017963': {'name': 'ad', 'age': 1, 'place': 'canada'},
     '49620712450163338969': {'name': 'dev', 'age': 1, 'place': 'texas'}}

# Extras

## Saving to a file

### Use `DB.commit(filename: str) -> None:` to save the DB to a file

```python
from pysondb import DB

db = DB(keys = ["name", "age", "place"])

db.add_many([
    {"name": "ad", "age": 1, "place": "canada"},
    {"name": "fred", "age": 2, "place": "canada"},
    {"name": "dev", "age": 1, "place": "texas"}
])

db.commit("test.json")
```

```python
cat test.json
```

    {
        "56391508197704412755": {
            "name": "ad",
            "age": 1,
            "place": "canada"
        },
        "34033319050367693482": {
            "name": "fred",
            "age": 2,
            "place": "canada"
        },
        "95561529227556367819": {
            "name": "dev",
            "age": 1,
            "place": "texas"
        }
    }

## Load values from a file

### Use `DB.load(filename: str) -> None:` to load the values from a file.

```python
from pysondb import DB

db = DB(keys=["name", "age", "place"])

db.load("test.json")
print(db)
```

    {'56391508197704412755': {'name': 'ad', 'age': 1, 'place': 'canada'},
     '34033319050367693482': {'name': 'fred', 'age': 2, 'place': 'canada'},
     '95561529227556367819': {'name': 'dev', 'age': 1, 'place': 'texas'}}

## Get the first 'n' values from the DB

### Use `DB.values(count: int = 5, last: bool = False) -> dict[str, dict[str, Any]]:`

```python
from pysondb import DB

db = DB(keys = ["name", "age"])

for i in range(10):
    db.add({"name": f"name{i}", "age": i})

print(db)

print(db.values())  # get the  first 5 values

print(db.values(count=3, last=True))  # get the last 3 values from the DB
```

    {'25450151252074394659': {'name': 'name0', 'age': 0},
     '90464346568236546790': {'name': 'name1', 'age': 1},
     '31876465304015561689': {'name': 'name2', 'age': 2},
     '56199458902278048668': {'name': 'name3', 'age': 3},
     '35022607077169707483': {'name': 'name4', 'age': 4},
     '24651900705643162239': {'name': 'name5', 'age': 5},
     '62441390413840228628': {'name': 'name6', 'age': 6},
     '51052354574257995704': {'name': 'name7', 'age': 7},
     '46451612512778442887': {'name': 'name8', 'age': 8},
     '70185518417588750000': {'name': 'name9', 'age': 9}}

    {'25450151252074394659': {'name': 'name0', 'age': 0}, '90464346568236546790': {'name': 'name1', 'age': 1}, '31876465304015561689': {'name': 'name2', 'age': 2}, '56199458902278048668': {'name': 'name3', 'age': 3}, '35022607077169707483': {'name': 'name4', 'age': 4}}

    {'51052354574257995704': {'name': 'name7', 'age': 7}, '46451612512778442887': {'name': 'name8', 'age': 8}, '70185518417588750000': {'name': 'name9', 'age': 9}}

## Using a custom id generator

### Use `DB.set_id_generator(func: Callable[[], str]) -> None:`

#### In this example we will be making a simple id generating function that gives incremental ids

```python
from pysondb import DB


id_count = 0
def get_id() -> str:
    global id_count
    id_count += 1
    return str(id_count)

db = DB(keys = ["name", "age"])
db.set_id_generator(get_id)

for i in range(10):
    db.add({"name": f"name{i}", "age": i})

print(db)
```

    {'1': {'name': 'name0', 'age': 0},
     '2': {'name': 'name1', 'age': 1},
     '3': {'name': 'name2', 'age': 2},
     '4': {'name': 'name3', 'age': 3},
     '5': {'name': 'name4', 'age': 4},
     '6': {'name': 'name5', 'age': 5},
     '7': {'name': 'name6', 'age': 6},
     '8': {'name': 'name7', 'age': 7},
     '9': {'name': 'name8', 'age': 8},
     '10': {'name': 'name9', 'age': 9}}

## Check whether an id exists in the DB

### Use `DB.id_exists(_id: str) -> bool:`

```python
from pysondb import DB

db = DB(keys = ["name", "age"])

id1 = db.add({"name": "ad", "age": 2})
id2 = db.add({"name": "fred", "age": 3})

print(db)

print(db.id_exists(id1))
print(db.id_exists("2324"))
```

    {'20395656516501272786': {'name': 'ad', 'age': 2},
     '63225287964423034893': {'name': 'fred', 'age': 3}}

    True
    False
