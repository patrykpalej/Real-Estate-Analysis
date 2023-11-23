from dataclasses import dataclass


@dataclass
class DomiportaSearchParams:
    """
    Common search params for all Domiporta offers, along with their default values
    """
    SortingOrder: str = "InsertionDate"
    RowsPerPage: int = "60"

    def set_param(self, param_name, param_value):
        self.__dict__[param_name] = param_value

    def to_dict(self):
        return {key: value
                for key, value in self.__dict__.items()
                if value is not None}


@dataclass
class DomiportaLotSearchParams(DomiportaSearchParams):
    pass


@dataclass
class DomiportaHouseSearchParams(DomiportaSearchParams):
    pass


@dataclass
class DomiportaApartmentSearchParams(DomiportaSearchParams):
    pass
