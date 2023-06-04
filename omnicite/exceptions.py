class OmniCiteException(Exception):
    pass


class OmniCiteSourceException(OmniCiteException):
    pass


class OmniCiteSourceFieldError(OmniCiteSourceException):
    pass


class OmniCiteWebError(OmniCiteException):
    pass


class ResourceNotFound(OmniCiteException):
    pass
