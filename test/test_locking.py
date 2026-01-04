import tempfile
from concurrent.futures import ThreadPoolExecutor
from tiny_data_warehouse.data_warehouse import DataWarehouse


def test_concurrent_writes_do_not_corrupt_parquet():
    """
    Business rule: Concurrent writes to the same parquet file must not corrupt it.
    
    Purpose: Validates that the FileLock mechanism prevents data corruption when
    multiple processes/threads attempt to write to the same event simultaneously.
    
    How it works:
    1. Creates a temporary DataWarehouse
    2. Spawns 10 threads that all write to the same event concurrently
    3. Verifies that all 10 rows are present and readable (no corruption)
    
    How to break this test:
    - Remove the FileLock from write_event() in data_warehouse.py
    - The concurrent writes will then race and corrupt the parquet file,
      resulting in either fewer rows or a read error
    """
    # setup
    with tempfile.TemporaryDirectory() as tmpdir:
        dw = DataWarehouse(events_folder=tmpdir)
        event_name = "concurrent_test"
        num_writers = 10

        def write_row(i: int):
            dw.write_event(event_name, {"value": f"row_{i}"})

        # perform
        with ThreadPoolExecutor(max_workers=num_writers) as executor:
            list(executor.map(write_row, range(num_writers)))

        # assert
        df = dw.event(event_name)
        assert len(df) == num_writers, f"Expected {num_writers} rows, got {len(df)}"
        
        # Verify all rows are present (no duplicates lost, no corruption)
        values = set(df["value"].tolist())
        expected_values = {f"row_{i}" for i in range(num_writers)}
        assert values == expected_values, f"Missing or corrupted rows: {expected_values - values}"
