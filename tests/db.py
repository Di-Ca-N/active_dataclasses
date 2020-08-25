from unittest import TestCase
from active_dataclasses.db import SQLiteDb
from sqlite3 import OperationalError


class DBTests(TestCase):
    def setUp(self):
        self.db = SQLiteDb(":memory:")
    
    def test_simple_table_creation(self):
        self.db.create_table(
            "person", {
                "cols": {
                    "id": (int, "INTEGER PRIMARY KEY"),
                    "name": (str, "TEXT"),
                    "age": (int, "INTEGER"),
                }, 
                "fks": {}
            }
        )
        self.assertRaises(OperationalError, self.db.execute_raw, "CREATE TABLE person();")

    def test_table_creation_with_foreign_key(self):
        self.db.create_table(
            "address", {
                "cols": {
                    "id": (int, "INTEGER PRIMARY KEY"),
                    "street": (str, "TEXT"),
                    "number": (int, "INTEGER"),
                }, 
                "fks": {}
            }
        )
        self.db.create_table(
            "person", {
                "cols": {
                    "id": (int, "INTEGER PRIMARY KEY"),
                    "name": (str, "TEXT"),
                    "age": (int, "INTEGER"),
                    "address": (int, "INTEGER")
                }, 
                "fks": {
                    "address": "address"
                }
            }
        )

    def test_db_select_all(self):
        self.db.create_table(
            "person", {
                "cols": {
                    "id": (int, "INTEGER PRIMARY KEY AUTOINCREMENT"),
                    "name": (str, "TEXT"),
                    "age": (int, "INTEGER"),
                }, 
                "fks": {}
            }
        )
        self.db.execute_raw("INSERT INTO person(name, age) VALUES ('John', 31), ('Peter', 10);")
        cursor = self.db.select('person')
        self.assertEqual(list(cursor), [(1, 'John', 31), (2, 'Peter', 10)])

    def test_db_select_with_filter(self):
        self.db.create_table(
            "person", {
                "cols": {
                    "id": (int, "INTEGER PRIMARY KEY AUTOINCREMENT"),
                    "name": (str, "TEXT"),
                    "age": (int, "INTEGER"),
                }, 
                "fks": {}
            }
        )
        self.db.execute_raw("INSERT INTO person(name, age) VALUES ('John', 31), ('Peter', 10);")
        cursor = self.db.select('person', name="John")
        self.assertEqual(list(cursor), [(1, 'John', 31)])
    
    def test_db_update(self):
        self.db.create_table(
            "person", {
                "cols": {
                    "id": (int, "INTEGER PRIMARY KEY AUTOINCREMENT"),
                    "name": (str, "TEXT"),
                    "age": (int, "INTEGER"),
                }, 
                "fks": {}
            }
        )
        self.db.execute_raw("INSERT INTO person(name, age) VALUES ('John', 31), ('Peter', 10);")
        self.db.update('person', 1, ('Mark',), ('name', ))
        self.assertEqual(list(self.db.select("person")), [(1, 'Mark', 31), (2, 'Peter', 10)])

    def test_db_delete(self):
        self.db.create_table(
            "person", {
                "cols": {
                    "id": (int, "INTEGER PRIMARY KEY AUTOINCREMENT"),
                    "name": (str, "TEXT"),
                    "age": (int, "INTEGER"),
                }, 
                "fks": {}
            }
        )
        self.db.execute_raw("INSERT INTO person(name, age) VALUES ('John', 31), ('Peter', 10);")
        self.db.delete('person', 1)
        self.assertEqual(list(self.db.select("person")), [(2, 'Peter', 10)])
