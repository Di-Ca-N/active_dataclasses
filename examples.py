from datetime import datetime
from active_dataclasses.models import persistent_dataclass

@persistent_dataclass
class Address:
    street: str
    number: int

    def get_person(self):
        return Person.manager.get(address=self.id)


@persistent_dataclass
class Person:
    name: str
    age: int
    address: Address
    birth_date: datetime
    awake: bool = False

    def __str__(self):
        return f"Person {self.name}: {(self.age, self.address, self.birth_date, self.awake)}"

    def get_address(self):
        return Address.manager.get(id=self.address)


address = Address('Foo St.', 50).save()
person = Person('John Doe', 30, address.id, datetime(2001, 11, 27, 0, 0, 0), True).save()
print(person)
print(person.get_address())
print(person.get_address().get_person())
person.name = "Paul"
person.save()
person.delete()

print(Person.manager.all())