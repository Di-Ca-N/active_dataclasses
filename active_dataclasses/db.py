import sqlite3
from datetime import date, datetime

from .utils import tuple_to_query, ConverterDict


class SQLiteDb:
    def __init__(self, db_name='db.sqlite'):
        self.db = sqlite3.connect(db_name)
        self.db.execute("PRAGMA foreign_keys = ON;")
        self.db.commit()
        self.data_types = {
            int: 'INTEGER',
            str: 'TEXT',
            float: 'REAL',
            bool: 'BOOLEAN',
            datetime: 'DATETIME',
            date: 'DATE',
        }
        self.data_converters = ConverterDict({
            datetime: datetime.fromisoformat,
            date: date.fromisoformat
        })

    def create_table(self, name, description):
        cols_txt = ', '.join(f'{field} {kind[1]}' for field, kind in description['cols'].items())
        single_fk_str = 'FOREIGN KEY ({}) REFERENCES {}(id)'
        fks_txt = ', '.join(single_fk_str.format(field, table) for field, table in description['fks'].items())
        table_txt = ', '.join(item for item in [cols_txt, fks_txt] if item)
        query = f'''CREATE TABLE IF NOT EXISTS {name}({table_txt});'''
        self.db.execute(query)
        self.db.commit()

    def insert(self, table, values, cols=None):
        query_placeholder = ','.join('?' for _ in values) 
        query = f"INSERT INTO {table}{tuple_to_query(cols)} VALUES ({query_placeholder});"
        cursor = self.db.execute(query, values)
        self.db.commit()
        return cursor.lastrowid

    def update(self, table, pk, values, cols):
        sets = ','.join(f'{col}=?' for col in cols)
        query = f"UPDATE {table} SET {sets} WHERE id=?;"
        self.db.execute(query, values + (pk, ))
        self.db.commit()

    def delete(self, table, pk):
        self.db.execute(f'DELETE FROM {table} WHERE id=?;', (pk, ))
        self.db.commit()

    def select(self, table, **where):
        where_str = ' AND '.join(f'{key}=?' for key in where)
        where_clause = f" WHERE {where_str}" if where_str else ""
        query = f'SELECT * FROM {table}{where_clause};'
        items = self.db.execute(query, tuple(where.values()))
        self.db.commit()
        return items
    
    def execute_raw(self, sql):
        return self.db.execute(sql)
