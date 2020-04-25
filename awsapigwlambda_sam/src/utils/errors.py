class Error(Exception):
    pass

class InvalidRequestError(Error):
    pass

class DataNotFoundError(Error):
    pass

class DocDBError(Error):
    pass