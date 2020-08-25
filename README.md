# Active Dataclasses

A simple ORM to turn easier the storage of data on small apps with simple models. Uses by default an SQLite 3 database (Contributing with other backends is very welcome :D). It is inspired on both Python dataclasses and Django ORM.

## Features

- Complete CRUD of models
- Simple syntax for model definition, based on Python's builtin data types
- Support for ForeignKey relations
- Queries by equality operation

## How to Use

It all starts by defining a model. To do this, simply use the annotations syntax (like in dataclasses), and all tables will be created

```python
from active_dataclasses import persistent_dataclass

@persistent_dataclass
class Address:
    street: str
    number: int


@persistent_dataclass
class Person:
    first_name: str
    last_name: str
    address: Address # This creates a foreign key to another table
    employment: str = "" # Field with default value
```

Dealing with objects:

```python
address = Address(street="4th Street", number=123) # Create an object
address.save() # Save it, assigning an id
person_1 = Person(first_name="John", last_name="Doe", address=address.id).save() # Create and save an object at the same time
Person(first_name="John", last_name="Doe", address=address.id).save()
Person(first_name="John", last_name="Mark", address=address.id).save()
Person(first_name="Foo", last_name="Barer", address=address.id).save()

# Filter - return a set of objects
Person.manager.filter(name="John")

# Get - return only one object (raises an error if more or less than one meets the conditions)
Person.manager.get(name="Foo")

# Delete - delete an object or collection of objects
Person.manager.all().delete()
```

## Supported data types

| Python Type       | Database Column Type |
| ----------------- | -------------------- |
| str               | TEXT                 |
| int               | INTEGER              |
| float             | REAL                 |
| bool              | BOOLEAN              |
| datetime.datetime | DATETIME             |
| datetime.date     | DATE                 |

If these column types doesn't fit your needs, you can choose another one of the supported types by the database backend, just by defining the wanted type on the annotations, as a string.

## Limitations

- Due to use of dataclasses, their limitations will be applied to your models too. One example is that you cannot define fields with default values after required fields.
- Only equality comparisons can be used on filters at this moment. (Work in Progress!)

## Testing

- Tests contributions are welcome
- To run the test suite, use `python -m unittest`
