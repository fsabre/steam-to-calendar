class STCException(Exception):
    """The base exception for steam-to-calendar"""
    pass


class TimeoutException(STCException):
    """The exception that occur when an operation is too long"""
    pass
