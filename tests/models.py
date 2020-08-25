from unittest import TestCase
from active_dataclasses.models import persistent_dataclass
from active_dataclasses.db import SQLiteDb


def test_persistent_dataclass(cls):
    test_db = SQLiteDb(':memory:')
    return persistent_dataclass(db=test_db)(cls)


class ModelSaveTest(TestCase):
    def setUp(self):
        @test_persistent_dataclass
        class Person:
            name: str
            age: int

        self.Person = Person

    def test_model_assigned_id_when_saves(self):
        person = self.Person("John Doe", 30).save()
        self.assertNotEqual(person.id, None)

    def test_model_get_returns_right_object(self):
        person = self.Person("John Doe", 31).save()
        self.Person("Mike", 32).save()
        retrieved_person = self.Person.manager.get(name="John Doe", age=31)
        self.assertEqual(person, retrieved_person)

    def test_model_filter_return_only_correct_objects(self):
        person_1 = self.Person("John Doe", 31).save()
        person_2 = self.Person("John Doe", 32).save()
        self.Person("Mike", 32).save()
        self.assertEqual(list(self.Person.manager.filter(name="John Doe")), [person_1, person_2])

    def tearDown(self):
        self.Person.manager.all().delete()