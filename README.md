# Installation

```sh
pip install tiny-data-warehouse
```


## Minimal usage


### Write events
```py
from tiny_data_warehouse import DataWarehouse
tdw = DataWarehouse()
tdw.write_event('person', {'name': 'Foo', 'age': 30})
```

### Read events

```py
from tiny_data_warehouse import DataWarehouse
tdw = DataWarehouse()
df = tdw.event('person')
df.head() # reads as pandas dataframe
```

or like a table

rom tiny_data_warehouse.base_table import BaseTable

```py

class TestTable(BaseTable):
    table_name = "test_table"
    schema = {
        'foo': {
            'type': 'string',
        },
        'bar': {
            'type': 'string',
        },
    }

def test_table():
    table = TestTable()
    entries = table.read()
    entries_count = len(entries)
    table.add(foo="foo", bar="bar")
    entries = table.read()
    assert len(entries) == entries_count + 1
```
