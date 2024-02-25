import os

from typing import Optional, List
import pandas as pd


DEFAULT_EVENTS_FOLDER = os.path.join(os.environ['HOME'], '.tinyws', 'events')

class DataWharehouse:
    def __init__(self, events_folder: Optional[str] = None, supported_events: Optional[List[str]]=None) -> None:
        if not events_folder:
            events_folder = DEFAULT_EVENTS_FOLDER
            print("Given that no events_folder was given, the default folder will be used: {}".format(events_folder))

        if not os.path.exists(events_folder):
            os.makedirs(events_folder)
            
        self.events_folder = events_folder
        self.supported_events = supported_events

    def list_stored_events(self) -> List[str]:
        os.system("ls -l {}".format(self.events_folder))

    def write_event(self, event_name, event: Optional[str]) -> None:
        """
        if event is a dict every key will be a column in the parquet file
        """
        if type(event) != dict:
            raise ValueError('event must be a dictionary got {}'.format(type(event)))

        df = pd.DataFrame([event])
        if os.path.exists(self._parquet_file(event_name)):
            df = pd.concat([pd.read_parquet(self._parquet_file(event_name)), df])
        df.to_parquet(self._parquet_file(event_name))


    def event(self, event_name: Optional[str]) -> pd.DataFrame:
        df = pd.read_parquet(self._parquet_file(event_name))

        return df

    def print_event(self, event_name: Optional[str]) -> None:
        print(self.event(event_name))
    
    def _parquet_file(self, event_name):
        return os.path.join(self.events_folder, event_name + '.parquet')
        

def main():
    import fire
    fire.Fire(DataWharehouse)

if __name__ == "__main__":
    main()
