# Installation

```sh
pip install tiny-data-warehouse
```


## Minimal usage


```py
# write event
from tiny_data_warehouse import DataWarehouse
tdw = DataWarehouse()
tdw.write_event('person', {'name': 'Foo', 'age': 30})
```



```py
from tiny_data_warehouse import DataWarehouse
df = tdw.event('person') # read events as pandas datafame
df.head()
```

