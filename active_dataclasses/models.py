from dataclasses import astuple, dataclass

from .db import SQLiteDb
from .utils import ColumnDescription


class Manager:
    def __init__(self, db, table_name, model):
        self.db = db
        self.table_name = table_name
        self.model = model

    def setup_table(self):
        self.db.create_table(self.model.table_name, self.model.describe())

    def save(self, data):
        cols = tuple(self.model.describe()['cols'].keys())[1:]
        values = astuple(data)[:-1]
        if data.id is None:
            data.id = self.db.insert(self.table_name, values, cols)
        else:
            self.db.update(self.table_name, data.id, values, cols)
        return data

    def delete(self, data):
        self.db.delete(self.table_name, data.id)

    def get(self, **filters):
        items = self.filter(**filters)
        if len(items) != 1:
            raise ValueError(f"'get' not returned only one object. It returned {len(items)}")
        return items[0]

    def all(self):
        return self.filter()

    def filter(self, **filters):
        return QueryResult(self.model, **filters)

    def _retrieve_data(self, **filters):
        items = self.db.select(self.table_name, **filters)
        columns = self.model.describe()['cols'].items()
        converted_data = [{col[0]: col[1].python_type(val) for col, val in zip(columns, item)} for item in items]
        data = [self.model(**model_data) for model_data in converted_data]
        return data


class Model:
    def __str__(self):
        return f'<{self.__class__.__name__} object(id={self.id})>'

    @classmethod
    def describe(cls):
        data = cls.__annotations__
        description = {'cols': {}, 'fks': {}}
        description['cols']['id'] = ColumnDescription(int, 'INTEGER PRIMARY KEY AUTOINCREMENT')
        for field, kind in data.items():
            if field == 'id':
                continue
            elif kind in cls.manager.db.data_types:
                description['cols'][field] = ColumnDescription(cls.manager.db.data_converters[kind], cls.manager.db.data_types[kind])
            elif hasattr(kind, 'describe'):
                description['cols'][field] = ColumnDescription(int, 'INTEGER')
                description['fks'][field] = f'{kind.table_name}'
            elif isinstance(kind, str):
                # Converter function that retrieve the data as it is saved on db
                description['cols'][field] = ColumnDescription(lambda x: x, kind)
            else:
                raise TypeError(f"Unknown field type: {kind}")
        return description

    def save(self):
        return self.manager.save(self)
    
    def delete(self):
        self.manager.delete(self)


def persistent_dataclass(*args, **kwargs):
    def real_decorator(model_class):
        db = kwargs.get('db', SQLiteDb())
        model_class = type(model_class.__name__, (Model,), dict(model_class.__dict__))
        model_class.id = None
        model_class.__annotations__['id'] = int
        model_class = dataclass(model_class)
        model_class.table_name = model_class.__name__.lower()
        model_class.manager = Manager(db, model_class.table_name, model_class)
        model_class.manager.setup_table()
        return model_class

    if kwargs.get('db') is None:
        return real_decorator(args[0])
    else:
        return real_decorator
        


class QueryResult:
    def __init__(self, model, **filters):
        self.model = model
        self.filters = filters
        self._results = None

    @property
    def results(self):
        if self._results is None:
            self._results = self._retrieve_data()
        return self._results

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.results})>"

    def __iter__(self):
        return iter(self.results)

    def __getitem__(self, index):
        return self.results[index]

    def save(self):
        for item in self.results:
            item.save()
        return self

    def delete(self):
        for item in self.results:
            item.delete()

    def filter(self, **filters):
        self.filters.update(filters)
        return self

    def get(self, **filters):
        self.filters.update(filters)
        return self._retrieve_data()

    def _retrieve_data(self):
        return self.model.manager._retrieve_data(**self.filters)
       