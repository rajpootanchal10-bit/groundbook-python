class GroundbookException(Exception):
    def __init__(self, status_code: int, error_type: str):
        self.status_code = status_code
        self.error_type = error_type

class NoSuchVenueException(GroundbookException):
    def __init__(self):
        super().__init__(404, "/errors/no-such-venue")

class NoSuchGroundException(GroundbookException):
    def __init__(self):
        super().__init__(404, "/errors/no-such-ground")

class ValidationException(GroundbookException):
    def __init__(self):
        super().__init__(400, "/errors/validation")