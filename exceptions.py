class InvalidInputException(Exception):
    """
    This Exception will be raised when we receive
    Invalid parameter from user
    """
    def __init__(self, message):
        super().__init__(message)


class DataNotPresent(Exception):
    """
    This Exception will be raised when we receive
    Invalid parameter from user
    """
    def __init__(self, message):
        super().__init__(message)


class ClientSideException(Exception):
    """
    This Exception will be raised when we receive
    client side (400's) status codes
    """
    def __init__(self, msg='Invalid Input', *args):
        super().__init__(msg, *args)


class ServerSideException(Exception):
    """
    This Exception will be raised when we receive
    server side (500's) status codes
    """
    def __init__(self, msg='Invalid Input', *args):
        super().__init__(msg, *args)


class RequestsErrorException(Exception):
    """
    This Exception will be raised when we receive
    status code other than 400's & 500's
    """
    def __init__(self, msg='Invalid Input', *args):
        super().__init__(msg, *args)
