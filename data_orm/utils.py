def tuple_to_query(tup):
    return f'({ ", ".join(str(item) for item in tup)})'