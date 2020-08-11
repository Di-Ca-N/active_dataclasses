# DataORM

A simple ORM to turn easier the storage of data on small apps with simple models. Uses by default an SQLite 3 database (Contributing with other backends is very welcome :D). It is inspired on both Python dataclasses and Django ORM.

## Features

- Complete CRUD of models
- Simple syntax for model definition, based on Python's builtin data types
- Support for ForeignKey relations

## How to Use

It all starts by defining a model. To do this, simply use the annotations syntax (like in dataclasses), and all tables will be created

```python
from data_orm.models import Model

@Model.register
class Address:
    street: str
    number: int


@Model.register
class Person:
    fist_name: str
    last_name: str
    address: Address # This creates a foreign key to another table
    employment: str = "" # Field with default value
```

## Supported data types

| Python Type       | Database Column |
| ----------------- | --------------- |
| str               | TEXT            |
| int               | INTEGER         |
| float             | REAL            |
| bool              | BOOLEAN         |
| datetime.datetime | DATETIME        |
| datetime.date     | DATE            |

If these column types doesn't fit your needs, you can choose another one from the supported by the database backend, just by defining the wanted type on the annotations

## Limitations

- Due to use of dataclasses as an underlying system, their limitations will be applied to your models too. One example is that you cannot define fields with default values after required fields.
- Only equality comparisons can be used on filters at this moment. (Work in Progress!)
