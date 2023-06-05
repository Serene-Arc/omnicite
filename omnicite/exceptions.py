class OmniCiteException(Exception):
    pass


class OmniCiteSourceException(OmniCiteException):
    pass


class OmniCiteAPIKeyMissing(OmniCiteSourceException):
    pass


class OmniCiteSourceFieldError(OmniCiteSourceException):
    pass


class OmniCiteWebError(OmniCiteException):
    pass


class ResourceNotFound(OmniCiteException):
    pass
