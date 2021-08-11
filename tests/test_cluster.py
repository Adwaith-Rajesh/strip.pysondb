import json
import os
from pathlib import Path

import pytest

from pysondb.cluster import Cluster
from pysondb.core import DB


CLUSTER_TEST_DATA = {
    "users": {
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
        },
    },
    "posts": {
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
        },
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

    users._db = CLUSTER_TEST_DATA["users"]
    posts._db = CLUSTER_TEST_DATA["posts"]

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

    assert c.users._db == CLUSTER_TEST_DATA["users"]
    assert c.posts._db == CLUSTER_TEST_DATA["posts"]


@pytest.mark.usefixtures("gen_cluster_data")
def test_cluster_load_selective():
    users = DB(keys=["name", "email"])
    # since only the users DB is a part of the cluster only that should be loaded
    c = Cluster({"users": users})
    c.load(CLUSTER_NAME)

    assert c.users._db == CLUSTER_TEST_DATA["users"]
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

    assert c.users._db == CLUSTER_TEST_DATA["users"]
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
