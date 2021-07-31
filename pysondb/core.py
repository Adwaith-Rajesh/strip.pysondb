import json
import typing
from pathlib import Path
from pprint import pformat
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from .utils import create_db
from .utils import generate_id
from .utils import verify_data


class DB:

    def __init__(self, filename: str, in_memory: bool = False) -> None:
        """Perform CRUD operations on a JSON DB"""

        # An in memory copy of the db
        self._db: Dict[str, Dict[str, Any]] = {}
        self._name = filename

        self._in_memory = in_memory

        if not in_memory:
            # create the DB if it does not exists
            create_db(self._name)
            self._load_json_db()

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

    def add(self, data: Dict[str, Any]) -> str:
        """Add a value to the DB"""

        if verify_data(self._v_data(data), data):
            _id = generate_id(list(self._db))
            self._db[_id] = data
            self._dump_db_to_json()
            return _id
        return "0"

    def add_many(self, data: List[Dict[str, Any]]) -> None:
        """Add more than one value to the DB at a time"""
        # steps to verify the data
        # 1) verify the first entry with DB
        # 2) then use the first entry to verify all the other entries.

        # if an of the entries in the list does not comply with the schema
        # , prevents all the other data from entering the DB
        db_clone = self._db.copy()

        # verify with the Db
        if verify_data(self._v_data(data[0]), data[0]):
            verified_data = data[0]

            for d in data:
                if verify_data(verified_data, d):
                    db_clone[generate_id(list(db_clone))] = d

            self._db = db_clone.copy()
            del [db_clone]
            self._dump_db_to_json()

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

    def update_by_id(self, _id: str, data: Dict[str, Any]) -> None:
        """Update a value by it id"""
        if self._db:
            if all(i in list(self._db.values())[0] for i in data):
                if _id in self._db:
                    self._db[_id].update(data)

                    self._dump_db_to_json()

            else:
                raise KeyError(
                    "Some keys provided in the update data does not match the keys in the DB"
                )

    def update_by_query(self, query: Dict[str, Any], new_data: Dict[str, Any]) -> List[str]:
        """Update values based on the query"""
        if self._db:
            if all(i in list(self._db.values())[0] for i in query) and all(
                i in list(self._db.values())[0] for i in new_data
            ):
                ids = list(
                    self.get_by_query(query)
                )  # get the ids of all the values that need to updated
                for i in ids:
                    self._db[i].update(new_data)

                self._dump_db_to_json()
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
        self._dump_db_to_json()

    def delete_all(self) -> None:
        """Delete all the values from the DB"""
        self._db.clear()
        self._dump_db_to_json()

    def delete_by_query(self, query: Dict[str, Any]) -> List[str]:
        """Delete values based on a query"""
        _ids = list(self.get_by_query(query).keys())
        for _id in _ids:
            self.delete_by_id(_id)
        self._dump_db_to_json()
        return _ids

    def force_save(self) -> None:
        """Forcefully save the DB as a JSON file
        usefull if the DB is in memory.
        """

        if self._in_memory:
            self._in_memory = False
            self._dump_db_to_json()
            self._in_memory = True

    ###############################################################################################

    def _load_json_db(self) -> None:
        """Loads the JSON file if it exists"""
        if not self._in_memory:
            if Path(self._name).is_file():
                try:
                    with open(self._name, "r") as f:
                        self._db = json.load(f)
                except json.decoder.JSONDecodeError:
                    self._db = {}

    def _dump_db_to_json(self) -> None:
        """dump the current instance of the DB in a file"""
        if not self._in_memory:
            with open(self._name, "w") as f:
                json.dump(self._db, f, indent=4)

    def _v_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Returns the data to cross validate with the data to be inserted
            data -> A sub value if the DB is empty.
        """
        return data if not self._db else list(self._db.values())[0]
