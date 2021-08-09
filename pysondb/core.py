import json
import typing
import warnings
from pathlib import Path
from pprint import pformat
from random import randint
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


class DB:

    def __init__(self, keys: List[str], verify_data: bool = True) -> None:
        """Perform CRUD operations on a JSON DB"""

        # An in memory copy of the db
        self._db: Dict[str, Dict[str, Any]] = {}
        self._verify = verify_data
        self._keys = sorted(keys)
        self._id_generator = self._generate_id

        # a flag to check whether any CRUD operation have been performed on the DB
        self._db_updated: bool = False

    @typing.no_type_check
    def __repr__(self) -> str:
        """A pretty format of the DB"""
        try:
            return pformat(self._db, sort_dicts=False, width=80)
        except TypeError:
            return pformat(self._db)

    def __len__(self) -> int:
        """Get the number of entries in the DB"""
        return len(self._db)

    def load(self, filename: str, force: bool = False) -> None:
        """Load an already existing DB"""
        if not self._db_updated or force is True:
            self._load_json_db(filename)
            self._db_updated = False

        else:
            warnings.warn(UserWarning(
                "You have un-committed data in your DB. This data will be lost during the "
                "loading of an external DB. If this is intentional use 'force=True'"), stacklevel=2)

    def commit(self, filename: str, indent: Optional[int] = None) -> None:
        """Store the current instance of the DB in a file"""
        self._dump_db_to_json(filename, indent=indent)
        self._db_updated = False

    def set_id_generator(self, func: Callable[[], str]) -> None:
        self._id_generator = func

    def id_exists(self, _id: str) -> bool:
        return _id in self._db

    def add(self, data: Dict[str, Any]) -> str:
        """Add a value to the DB"""

        if self._verify_data(data):
            _id = str(self._id_generator())
            self._db[_id] = data
            self._db
            self._db_updated = True
            return _id
        return "0"

    def add_many(self, data: List[Dict[str, Any]]) -> None:
        """Add more than one value to the DB at a time"""

        if self._verify:
            for d in data:
                self._verify_data(d)

        for d in data:
            self._db[str(self._id_generator())] = d

        self._db_updated = True

    def get_by_id(self, _id: str) -> Union[None, Dict[str, Any]]:
        """Get the value from the DB based on the _id"""
        _id = str(_id)
        if _id in self._db:
            return self._db[_id]

        return None

    def get_by_query(self, query: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Get the values from the DB based on the query conditions"""
        return {
            i: x
            for i, x in self._db.items()
            if all(k in x and x[k] == v for k, v in query.items())
        }

    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """Returns the entire DB"""
        return self._db.copy()

    def pop(self, _id: str) -> Union[None, Dict[str, Any]]:
        """Remove and return item of the specified id"""

        data = self.get_by_id(_id)
        self.delete_by_id(_id)
        self._db_updated = True
        return data

    def values(self, count: int = 5, last: bool = False) -> Dict[str, Dict[str, Any]]:
        if not last:
            keys = list(self._db)[:count]
        else:
            keys = list(self._db)[-count:]

        return {i: self._db[i] for i in keys}

    def update_by_id(self, _id: str, data: Dict[str, Any]) -> None:
        """Update a value by it id"""
        if self._db:
            if all(i in self._keys for i in data):
                if _id in self._db:
                    self._db[_id].update(data)
                    self._db_updated = True
            else:
                raise KeyError(
                    "Some keys provided in the update data does not match the keys in the DB"
                )

    def update_by_query(self, query: Dict[str, Any], new_data: Dict[str, Any]) -> List[str]:
        """Update values based on the query"""
        if self._db:
            if all(i in self._keys for i in query) and all(i in self._keys for i in new_data):
                ids = list(
                    self.get_by_query(query)
                )  # get the ids of all the values that need to updated
                for i in ids:
                    self._db[i].update(new_data)
                self._db_updated = True
                return ids

            else:
                raise KeyError(
                    "The key in the query or the key in the new_data does not match the keys in the DB"
                )
        return []

    def delete_by_id(self, _id: str) -> None:
        """Delete values based in id"""
        if _id in self._db:
            del self._db[_id]
            self._db_updated = True

    def delete_all(self) -> None:
        """Delete all the values from the DB"""
        self._db.clear()
        self._db_updated = True

    def delete_by_query(self, query: Dict[str, Any]) -> List[str]:
        """Delete values based on a query"""
        _ids = list(self.get_by_query(query).keys())
        for _id in _ids:
            self.delete_by_id(_id)
        self._db_updated = True
        return _ids
    ###############################################################################################

    def _generate_id(self) -> str:
        _id = randint(int("1" + "0" * 19), int("9" * 20))

        while str(_id) in self._db:
            _id = randint(int("1" + "0" * 19), int("9" * 20))

        return str(_id)

    def _load_json_db(self, filename: str) -> None:
        """Loads the JSON file if it exists"""
        if Path(filename).is_file():
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                    for val in data.values():
                        self._verify_data(val)

                    self._db = data.copy()

            except json.decoder.JSONDecodeError:
                self._db = {}

    def _dump_db_to_json(self, filename: str, indent: Optional[int] = None) -> None:
        """dump the current instance of the DB in a file"""
        with open(filename, "w") as f:
            json.dump(self._db, f, indent=indent)

    def _verify_data(self, data: Dict[str, Any]) -> bool:
        """verify whether the data provided has the same keys
         as provided in the keys list"""

        if self._verify:
            if self._keys == sorted(data.keys()):
                return True

            else:
                raise KeyError(
                    "The keys provided in the data does not match the provided keys.")

        return True
