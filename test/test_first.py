

from tiny_data_wharehouse.data_wharehouse import DataWharehouse


def test_first():

    dwh = DataWharehouse('/tmp/events')
    dwh.write_event('Test', {'foo': 'bar'})
    dwh.write_event('Test', {'foo': 'baz'})
    result =dwh.event('Test')
    print('Loaded event', result)
