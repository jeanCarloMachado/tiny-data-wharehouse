import os

from typing import Optional
import pandas as pd

class DataWarehouse:
    DEFAULT_FOLDER = os.path.join(os.environ['HOME'], '.tinyws')
    DEFAULT_EVENTS_FOLDER = os.path.join(DEFAULT_FOLDER, 'events')

    def __init__(self, events_folder: Optional[str] = None, events_config=None) -> None:
        if not events_folder:
            events_folder = DataWarehouse.DEFAULT_EVENTS_FOLDER

        if not os.path.exists(events_folder):
            os.makedirs(events_folder)
            
        self.base_folder = DataWarehouse.DEFAULT_FOLDER
        self.events_folder = events_folder
        self.events_config = events_config
        if events_config:
            print("Events config given: ", events_config)

    def list_stored_events(self):
        os.system("ls -l {}".format(self.events_folder))

    def write_event(self, event_name: str, event_data: dict, verbose=False, dry_run=False) -> None:
        """
        if event is a dict every key will be a column in the parquet file

        Adds a column tdw_timestamp to the event
        """
        self._validate_event_data(event_data)

        event_data['tdw_timestamp'] = pd.Timestamp.now()
        new_df = pd.DataFrame([event_data])

        if self._exists_data(event_name):
            existing_data = self.event(event_name)

            if event_name in self.events_config and 'prevent_duplicates_col' in self.events_config[event_name]:
                check_column_name = self.events_config[event_name]['prevent_duplicates_col']
                possible_duplicated_value = event_data[check_column_name]

                # test if in existing_data there is a duplicated value
                if possible_duplicated_value in existing_data[check_column_name].values:
                    raise ValueError(f"A duplicated value {event_data[check_column_name]} for key {check_column_name} was found in the event {event_name}")

            df = pd.concat([existing_data, new_df])

        if not dry_run:
            self._write_df(event_name, df)
        else:
            print(f"Event {event_name} written successfully")

        if verbose:
            print(f"Event {event_name} written successfully")

    def _write_df(self, event_name, df):
        df.to_parquet(self._parquet_file(event_name))

    def _validate_event_data(self, event_data: dict) -> None:
        if type(event_data) != dict:
            raise ValueError('event must be a dictionary got {}'.format(type(event_data)))

    def _exists_data(self, event_name: str) -> bool:
        return os.path.exists(self._parquet_file(event_name))

    def event(self, event_name: Optional[str]) -> pd.DataFrame:
        """
        Reads the data from the event returned as a pandas DataFrame
        """
        if not os.path.exists(self._parquet_file(event_name)):
            raise ValueError('Event {} does not exist'.format(event_name))

        df = pd.read_parquet(self._parquet_file(event_name))

        return df

    def replace_df(self, event_name: str, df: pd.DataFrame, dry_run=True) -> None:
        if dry_run:
            print('Replace of event {}, destructive event! Disable dry run to execute it'.format(event_name))
        df.to_parquet(self._parquet_file(event_name))

    def remove_event(self, event_name: str, dry_run=True) -> None:
        if dry_run:
            print('Dry run removal of the the event {}, destructive event! Disable dry run to execute it'.format(event_name))

        os.remove(self._parquet_file(event_name))

    def print_event(self, event_name: Optional[str]) -> None:
        print(self.event(event_name))
    
    def _parquet_file(self, event_name):
        return os.path.join(self.events_folder, event_name + '.parquet')
        

def main():
    import fire
    fire.Fire(DataWarehouse)

if __name__ == "__main__":
    main()
