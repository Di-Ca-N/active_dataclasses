from collections import UserDict, namedtuple


def tuple_to_query(tup):
    return f'({ ", ".join(str(item) for item in tup)})'


class ConverterDict(UserDict):
    def __missing__(self, key):
        return key


ColumnDescription = namedtuple('ColumnDescription', ('python_type', 'db_type'))
