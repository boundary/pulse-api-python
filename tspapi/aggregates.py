# -*- coding: utf-8 -*-

from requests.structures import LookupDict

_aggregates = {

    # Informational.
    'AVG': ('AVG',),
    'MAX': ('MAX',),
    'MIN': ('MIN',),
    'SUM': ('SUM',),
}

aggregates = LookupDict(name='status_codes')

for code, titles in _aggregates.items():
    for title in titles:
        setattr(aggregates, title, code)
        if not title.startswith('\\'):
            setattr(aggregates, title.upper(), code)
