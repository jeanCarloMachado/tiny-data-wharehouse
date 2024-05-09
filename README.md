# Installation

```
pip install tiny-data-warehouse
```


## Minimal usage


```py

from tiny_data_warehouse import DataWarehouse
import pandas as pd

# write event
tdw = DataWarehouse()
tdw.write_event('person', {'name': 'Foo', 'age': 30})


# read events
df : pd.DataFrame = tdw.event('person')
df.head()

```

