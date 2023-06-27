import json
import pandas as pd
from dataclasses import dataclass


@dataclass
class Offer:
    def to_dict(self, parse_json: bool = False):
        if not parse_json:
            return self.__dict__

        output_dict = {}
        for key, value in self.__dict__.items():
            try:
                value = json.loads(value)
            except TypeError:
                value = value
            except json.decoder.JSONDecodeError:
                value = value

            output_dict[key] = value

        return output_dict

    def to_dataframe(self):
        data_dict = {k: [v] for k, v in self.to_dict().items()}
        return pd.DataFrame(data_dict)
