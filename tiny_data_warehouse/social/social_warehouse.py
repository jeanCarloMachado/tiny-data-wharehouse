import pandas as pd

class SocialWarehouse:

    data = {
        'world_bank.gdp': {
            'path': "/Users/jean.machado/projects/tiny-data-warehouse/local_data/gdp/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_401130.csv",
        }
    }

    def read(self, event_name: str) -> pd.DataFrame:
        if not event_name in self.data:
            raise ValueError(f"Event {event_name} does not exist")

        return pd.read_csv(self.data[event_name]['path'])