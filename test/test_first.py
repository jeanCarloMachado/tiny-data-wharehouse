

from tiny_data_warehouse.data_warehouse import DataWarehouse

def test_first():

    dwh = DataWarehouse('/tmp/events')
    dwh.write_event('Test', {'foo': 'bar'})
    dwh.write_event('Test', {'foo': 'baz'})
    result =dwh.event('Test')
    print('Loaded event', result)
