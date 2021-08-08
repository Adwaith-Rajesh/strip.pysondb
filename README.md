# strip.pysondb

[![GitHub](https://img.shields.io/github/license/Adwaith-Rajesh/strip.pysondb?style=for-the-badge)](https://github.com/Adwaith-Rajesh/strip.pysondb/blob/master/LICENSE)
[![Azure DevOps builds](https://img.shields.io/azure-devops/build/adwaithrajesh/8d11fcc8-9bf7-41cf-95af-bd240456c13e/8?label=azure%20pipeline&style=for-the-badge)](https://dev.azure.com/adwaithrajesh/adwaith/_build?definitionId=8)
[![PyPI](https://img.shields.io/pypi/v/strip.pysondb?style=for-the-badge)](https://pypi.org/project/strip.pysondb/)

A stripped-down version of [pysondb](https://github.com/fredysomy/pysonDB) by [Fredy Somy](https://github.com/fredysomy).

---

## Features.

- No third party packages needed
- No CLI
- No ImageUtils
- Use of [python naming conventions](https://www.python.org/dev/peps/pep-0008/#function-and-variable-names) in functions and classes.
- Just the code required to perform CRUD operation on JSON DB.
- Users can generate custom id's for their data.

## Note

Even though it's called a stripped-down version, there are some huge differences in the way this package works.

- The data is not saved to file instantly, instead a methods needs to be called in order to do that.
- The user is supposed to pass the keys / column name for the DB during initialization of the `DB` class.
- Some of the new methods that are not derived from PysonDB are,
  - `pop`
  - `commit`
  - `load`
  - `values`
  - `set_id_generator`

---

## Installation

- ### Delete the original pysondb before installing this version. (Might cause conflicts)

- ### From Pypi
  ```commandline
  pip3 install strip.pysondb
  ```

---

## Usage

- ## tl;dr

  ```python
  from pysondb import DB

  db = DB(keys = ["name", "age"])
  db.add({
      "name": "name1",
      "age": 1
  })

  print(db)

  ```

### Click [here](https://github.com/Adwaith-Rajesh/strip.pysondb/blob/master/docs/docs.md) to see the complete docs.

---

<h3 align="center"> <img align="center" src="https://forthebadge.com/images/badges/made-with-python.svg" href="https://python.org" ></h3>
