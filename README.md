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

