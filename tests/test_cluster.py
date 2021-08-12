import json
import os
from pathlib import Path

import pytest

from pysondb.cluster import Cluster
from pysondb.core import DB


CLUSTER_TEST_DATA = {
    "users": {
        "keys": ["email", "name"],
        "data": {
            "123456": {
                "name": "test",
                        "email": "test@g.com"
            },
            "237648": {
                "name": "ad",
                        "email": "ad@y.com"
            },
            "237380": {
                "name": "fred",
                        "email": "fred@prox.com"
            }
        }
    },
    "posts": {
        "keys": ["by", "content", "title"],
        "data": {
            "267276": {
                "by": "test",
                "title": "hello",
                "content": "hello World"
            },
            "263273": {
                "by": "ad",
                "title": "bye",
                "content": "Bye World"
            },
            "227276": {
                "by": "fred",
                "title": "good",
                "content": "good World"
            }
        }
    }
}

CLUSTER_NAME = "test.cluster.json"
def remove_file(): return os.remove(CLUSTER_NAME)


@pytest.fixture
def rm_file():
    yield
    remove_file()


@pytest.fixture
def gen_cluster_data():
    with open(CLUSTER_NAME, "w") as f:
        json.dump(CLUSTER_TEST_DATA, f)

    yield
    remove_file()


def test_cluster_init():
    users = DB(keys=["name", "email"])
    posts = DB(keys=["by", "title", "content"])

    try:
        _ = Cluster({"users": users, "posts": posts})

    except ValueError:
        pytest.fail("ValueError raised with non empty dbs")


@pytest.mark.parametrize(
    "test_input",
    (
        {},
        {"name": "test"},
        {"test": 2},
        {"check": {}}
    )
)
def test_cluster_init_value_error(test_input):
    # raised when the cluster dbs is empty
    # or dbs values are not of type DB

    with pytest.raises(ValueError):
        _ = Cluster(test_input)


def test_cluster_init_key_error():
    # Raised when the keys are not of type str
    with pytest.raises(KeyError):
        _ = Cluster({1: DB(keys=["t"])})


@pytest.mark.usefixtures("rm_file")
def test_cluster_commit():
    users = DB(keys=["name", "email"])
    posts = DB(keys=["by", "title", "content"])

    users._db = CLUSTER_TEST_DATA["users"]["data"]
    posts._db = CLUSTER_TEST_DATA["posts"]["data"]

    c = Cluster({"users": users, "posts": posts})
    c.commit(CLUSTER_NAME)

    assert Path(CLUSTER_NAME).is_file()
    with open(CLUSTER_NAME, "r") as f:
        assert json.load(f) == CLUSTER_TEST_DATA


@pytest.mark.usefixtures("gen_cluster_data")
def test_cluster_load():
    users = DB(keys=["name", "email"])
    posts = DB(keys=["by", "title", "content"])

    c = Cluster({"users": users, "posts": posts})
    c.load(CLUSTER_NAME)

    assert c.users._db == CLUSTER_TEST_DATA["users"]["data"]
    assert c.posts._db == CLUSTER_TEST_DATA["posts"]["data"]


@pytest.mark.usefixtures("gen_cluster_data")
def test_cluster_load_selective():
    users = DB(keys=["name", "email"])
    # since only the users DB is a part of the cluster only that should be loaded
    c = Cluster({"users": users})
    c.load(CLUSTER_NAME)

    assert c.users._db == CLUSTER_TEST_DATA["users"]["data"]
    assert c.posts is None


@pytest.mark.usefixtures("gen_cluster_data")
def test_cluster_load_error():
    users = DB(keys=["name"])
    c = Cluster({"users": users})

    with pytest.raises(KeyError):
        c.load(CLUSTER_NAME)


@pytest.mark.usefixtures("gen_cluster_data")
def test_cluster_crud():
    users = DB(keys=["name", "email"])
    c = Cluster({"users": users})
    c.load(CLUSTER_NAME)

    assert c.users._db == CLUSTER_TEST_DATA["users"]["data"]
    c.users.get_by_id("123456") == {
        "name": "test",
        "email": "test@g.com"
    }

    c.users.update_by_id("237648", {"name": "admin"})
    assert c.users._db["237648"] == {
        "name": "admin",
        "email": "ad@y.com"
    }

    c.users.delete_by_id("237380")
    assert c.users._db == {
        "123456": {
            "name": "test",
            "email": "test@g.com"
        },
        "237648": {
            "name": "admin",
            "email": "ad@y.com"
        }}


def test_cluster_print_single_db(capsys):
    db = DB(keys=["test"])
    c = Cluster({"db": db})
    print(c)

    out, err = capsys.readouterr()
    assert out == "A Cluster of { db }\n"
    assert err == ""


def test_cluster_print_multiple_db(capsys):
    users = DB(keys=["name", "email"])
    posts = DB(keys=["by", "title", "content"])

    c = Cluster({"users": users, "posts": posts})

    print(c)
    out, err = capsys.readouterr()
    assert out == "A Cluster of { users, posts }\n"
    assert err == ""


def test_cluster_databases_property():
    c = Cluster({"users": DB(keys=[]), "posts": DB(keys=[])})
    assert c.databases == ["posts", "users"]


@pytest.mark.usefixtures("gen_cluster_data")
def test_cluster_load_dynamic():
    c = Cluster(dbs={}, dynamic=True)

    c.load(CLUSTER_NAME)
    assert c._d_loading is True
    assert c.databases == ["posts", "users"]
    assert c.posts._db == CLUSTER_TEST_DATA["posts"]["data"]
    assert c.users._db == CLUSTER_TEST_DATA["users"]["data"]


@pytest.mark.usefixtures("rm_file")
def test_cluster_load_json_decode_warning():
    with open(CLUSTER_NAME, "w") as f:
        f.write("{")

    c = Cluster(dbs={}, dynamic=True)

    with pytest.warns(UserWarning):
        c.load(CLUSTER_NAME)


def test_cluster_add_db():
    c = Cluster(dbs={}, dynamic=True)

    assert c.databases == []
    c.add_db("test", DB(keys=["test"]))
    assert c.databases == ['test']
    assert c.test.keys == ["test"]


def test_cluster_add_db_warning():
    c = Cluster(dbs={"test": DB(keys=["test"])})

    with pytest.warns(UserWarning):
        c.add_db("test", DB(keys=[]))


@pytest.mark.parametrize(
    "k,v",
    (
        (1, "d"),
        (2, 3),
        ("Str", 4)
    )
)
def test_cluster_value_error(k, v):
    c = Cluster(dbs={}, dynamic=True)

    with pytest.raises(ValueError):
        c.add_db(k, v)


def test_cluster_delete_db():
    c = Cluster(dbs={"test": DB(keys=["test"])}, dynamic=True)

    assert c.databases == ["test"]
    c.delete_db("test")
    assert c.databases == []


def test_cluster_delete_db_warning():
    c = Cluster(dbs={"test": DB(keys=["test"])})

    with pytest.warns(UserWarning):
        c.delete_db("test")
