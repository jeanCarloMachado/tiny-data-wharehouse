# Tiny Data Warehouse

[![PyPI version](https://badge.fury.io/py/tiny-data-warehouse.svg)](https://badge.fury.io/py/tiny-data-warehouse)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, file-based data warehouse for Python projects. Store and query your data locally using Parquet files with zero configuration.

## ✨ Features

- **Zero Configuration** — Works out of the box with sensible defaults
- **Parquet Storage** — Efficient columnar storage format for fast reads
- **Pandas Integration** — Seamless integration with pandas DataFrames
- **Schema Validation** — Optional schema-based tables with type checking
- **CLI Support** — Command-line interface for quick data inspection
- **Backup & Restore** — Built-in backup functionality for data safety
- **Duplicate Prevention** — Optional duplicate detection on specified columns

## 📦 Installation

```sh
pip install tiny-data-warehouse
```

## 🚀 Quick Start

### Writing Events

```python
from tiny_data_warehouse import DataWarehouse

tdw = DataWarehouse()
tdw.write_event('users', {'name': 'Alice', 'age': 30, 'city': 'Berlin'})
tdw.write_event('users', {'name': 'Bob', 'age': 25, 'city': 'London'})
```

### Reading Events

```python
from tiny_data_warehouse import DataWarehouse

tdw = DataWarehouse()
df = tdw.event('users')
print(df)
#     name  age    city              tdw_timestamp                            tdw_uuid
# 0  Alice   30  Berlin  2024-01-15 10:30:00.123456  550e8400-e29b-41d4-a716-446655440000
# 1    Bob   25  London  2024-01-15 10:30:01.234567  6fa459ea-ee8a-3ca4-894e-db77e160355e
```

Every event automatically includes:
- `tdw_timestamp` — When the event was recorded
- `tdw_uuid` — Unique identifier for each event

## 📋 Schema-Based Tables

For more structured data, use `BaseTable` to define schemas with validation:

```python
from tiny_data_warehouse.base_table import BaseTable

class UserTable(BaseTable):
    table_name = "users"
    schema = {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'active': {'type': 'boolean'},
    }

# Create and use the table
users = UserTable()
users.add(name="Alice", email="alice@example.com", active=True)

# Read all records
df = users.read()

# Query specific records
active_users = users.load_with_value('active', True)

# Get the most recent entry
latest = users.last()

# Update existing records
users.update(by_key='email', by_value='alice@example.com', new_values={'active': False})

# Delete records
users.delete_by(column='email', value='alice@example.com')
```

### BaseTable API

| Method | Description |
|--------|-------------|
| `add(**kwargs)` | Add a new record (returns `tdw_uuid`) |
| `read(recent_first=False)` | Read all records as DataFrame |
| `load_with_value(column, value)` | Filter records by column value |
| `last()` | Get the most recent record |
| `len()` / `length()` | Count total records |
| `is_empty()` | Check if table has no records |
| `update(by_key, by_value, new_values)` | Update existing record |
| `update_or_create(by_key, by_value, new_values)` | Update or insert record |
| `delete_by(column, value)` | Delete records matching criteria |
| `reset(dry_run=True)` | Clear all records |
| `replace(df, dry_run=True)` | Replace entire table with DataFrame |
| `add_column(column_name, default_value)` | Add new column to existing data |

## 🔧 Configuration

### Custom Storage Location

```python
from tiny_data_warehouse import DataWarehouse

# Default: ~/.tinyws/events/
tdw = DataWarehouse(events_folder='/path/to/your/data')
```

### Duplicate Prevention

Prevent duplicate entries based on a specific column:

```python
tdw = DataWarehouse(events_config={
    'users': {
        'prevent_duplicates_col': 'email'
    }
})

tdw.write_event('users', {'email': 'alice@example.com', 'name': 'Alice'})
tdw.write_event('users', {'email': 'alice@example.com', 'name': 'Alice 2'})  # Raises ValueError
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `TINYWS_CREATE_EMPTY_WHEN_NOT_FOUND` | Return empty DataFrame instead of raising error for missing events |

## 💻 Command Line Interface

Tiny Data Warehouse includes a CLI for quick data operations:

```sh
# List all stored events
tdw list_stored_events

# Print event data
tdw print_event users

# Create a backup
tdw backup_all

# List available backups
tdw backups_list

# Restore from backup
tdw backup_restore 2024-01-15_10-30-00
```

## 🔄 Backup & Restore

```python
tdw = DataWarehouse()

# Create a timestamped backup
tdw.backup_all()

# List available backups
tdw.backups_list()

# Restore from a specific backup
tdw.backup_restore('2024-01-15_10-30-00', dry_run=False)
```

## 📁 Data Storage

By default, data is stored in `~/.tinyws/events/` as Parquet files:

```
~/.tinyws/
└── events/
    ├── users.parquet
    ├── orders.parquet
    └── products.parquet
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

```sh
# Clone the repository
git clone https://github.com/your-username/tiny-data-warehouse.git
cd tiny-data-warehouse

# Install dependencies
poetry install

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
