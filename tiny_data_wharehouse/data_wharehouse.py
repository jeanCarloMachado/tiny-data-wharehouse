

from typing import Optional, List


class DataWharehouse:
    def __init__(self, events_folder: Optional[str] = None, supported_events: Optional[List[str]]=None) -> None:
        self.events_folder = events_folder
        self.supported_events = supported_events


    def write_event(self, event, event_name: Optional[str]) -> None:
        pass