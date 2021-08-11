The main use case of a cluster, is way to combine multiple DB that kind of revolves around the same "object".
For example let's say you are making a blog that allows people to post, follow others etc.
So a cluster for a user will contain a db to track all the post they made. a DB to track all of followers / following etc.

```python
from pysondb import Cluster
from pysondb import DB

posts = DB(keys=["title", "content"])
followers = DB(keys=["name", "followed-on"])

c = Cluster({"posts": posts, "followers": followers})  # initialize a cluster, in this case for a user

c.posts.add({"title": "hello", "content": "Hello WOrld"})  # all the CRUD methods will work in the cluster
print(c.posts)

c.commit("user1.json", indent=2)  # save the cluster for a specific user

```

    {'55612354709877511652': {'title': 'hello', 'content': 'Hello WOrld'}}

```python
cat user1.json
```

    {
      "posts": {
        "55612354709877511652": {
          "title": "hello",
          "content": "Hello WOrld"
        }
      },
      "followers": {}
    }

#### Loading a cluster

```python
from pysondb import Cluster
from pysondb import DB

posts = DB(keys=["title", "content"])
followers = DB(keys=["name", "followed-on"])

c = Cluster({"posts": posts, "followers": followers})
c.load("user1.json")

print(c.posts)
print(c.followers)
```

    {'55612354709877511652': {'title': 'hello', 'content': 'Hello WOrld'}}
    {}

The cluster loading is a selective process, meaning it will only load the clusters mentioned during the init of the cluster.

The `user1.json` currently contains data for two DB. but you can load only one DB with the following code

```python
from pysondb import Cluster
from pysondb import DB

posts = DB(keys=["title", "content"])

c = Cluster({"posts": posts})
c.load("user1.json")

print(c.posts)
print(c.followers)
```

    {'55612354709877511652': {'title': 'hello', 'content': 'Hello WOrld'}}
    None

### Dynamic cluster loading

This feature is useful if you have no idea about the data in a cluster

```python
from pysondb import Cluster

c = Cluster(dbs={}, dynamic=True)
c.load("user1.json")

print(c.databases)
print(c.posts)
```

    ['followers', 'posts']
    {'71759298542570006049': {'title': 'hello', 'content': 'Hello WOrld'}}

---

<h1 align="center"> Have fun 🥰. </h1>
