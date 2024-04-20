import os

from typing import Optional, List
import pandas as pd


DEFAULT_FOLDER = os.path.join(os.environ['HOME'], '.tinyws')
DEFAULT_EVENTS_FOLDER = os.path.join(DEFAULT_FOLDER, 'events')

class DataWarehouse:
    def __init__(self, events_folder: Optional[str] = None, supported_events: Optional[List[str]]=None) -> None:
        if not events_folder:
            events_folder = DEFAULT_EVENTS_FOLDER
            #print("Given that no events_folder was given, the default folder will be used: {}".format(events_folder))

        if not os.path.exists(events_folder):
            os.makedirs(events_folder)
            
        self.base_folder = DEFAULT_FOLDER
        self.events_folder = events_folder
        self.supported_events = supported_events


    def list_stored_events(self) -> List[str]:
        os.system("ls -l {}".format(self.events_folder))

    def ls(self):
        return self.list_stored_events()

    def write_event(self, event_name, event: Optional[str]) -> None:
        """
        if event is a dict every key will be a column in the parquet file

        Adds a column tdw_timestamp to the event
        """
        if type(event) != dict:
            raise ValueError('event must be a dictionary got {}'.format(type(event)))

        event['tdw_timestamp'] = pd.Timestamp.now()
        df = pd.DataFrame([event])
        if os.path.exists(self._parquet_file(event_name)):
            df = pd.concat([pd.read_parquet(self._parquet_file(event_name)), df])
        df.to_parquet(self._parquet_file(event_name))
        print(f"Event {event_name} written successfully")


    def event(self, event_name: Optional[str]) -> pd.DataFrame:
        """
        Reads the data from the event returned as a pandas DataFrame
        """
        if not os.path.exists(self._parquet_file(event_name)):
            raise ValueError('Event {} does not exist'.format(event_name))

        df = pd.read_parquet(self._parquet_file(event_name))

        return df

    def remove_event(self, event_name: str, dry_run=True) -> None:

        if dry_run:
            print('Dry run removal of the the event {}. Disable dry run to execute it'.format(event_name))

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
