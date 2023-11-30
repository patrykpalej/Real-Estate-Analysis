from dataclasses import dataclass


@dataclass
class OtodomSearchParams:
    """
    Common search params for all Otodom offers, along with their default values
    """
    ownerTypeSingleSelect: str = "ALL"
    limit: int = "72"
    daysSinceCreated: int = 1
    by: str = "LATEST"
    direction: str = "DESC"
    viewType: str = "listing"
    priceMin: int = None
    priceMax: int = None

    def set_param(self, param_name, param_value):
        self.__dict__[param_name] = param_value

    def to_dict(self):
        return {key: value
                for key, value in self.__dict__.items()
                if value is not None}


@dataclass
class OtodomLandSearchParams(OtodomSearchParams):
    areaMin: int = None
    areaMax: int = None
    plotType: str = "[BUILDING]"
    pricePerMeterMin: int = None
    pricePerMeterMax: int = None


@dataclass
class OtodomHouseSearchParams(OtodomSearchParams):
    pass


@dataclass
class OtodomApartmentSearchParams(OtodomSearchParams):
    pass
