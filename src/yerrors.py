class YError(Exception): ...


class YInternalError(YError): ...


class YInvalidLoggingError(YInternalError): ...


class YInvalidRegexesError(YInternalError): ...


class YInvalidChecksError(YInternalError): ...


class YExternalError(YError): ...


class YBadSyntaxError(YExternalError): ...
