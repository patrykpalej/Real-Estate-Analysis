class ServiceNotExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidOffer(Exception):
    def __init__(self, message):
        super().__init__(message)


class AlreadyStoredOffer(Exception):
    def __init__(self, message):
        super().__init__(message)
