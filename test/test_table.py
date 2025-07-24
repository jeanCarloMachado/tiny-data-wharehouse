from tiny_data_warehouse.base_table import BaseTable


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