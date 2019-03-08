class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class UnknownError(Error):

    def __init__(self, text=''):
        message = 'An internal error has occurred. Please try your query again at a later time.'
        if text == '':
            log_message = 'Unknown error occurred. Perhaps the cause may be a code bug'
        else:
            log_message = text
        Exception.__init__(self, message)
        self.code = 'InternalError'
        self.log_message = log_message


class StorageServiceError(Error):

    def __init__(self, param=''):
        if param == '':
            message = 'An internal error has occurred. Please try your query again at a later time.'
            log_message = 'Storage service error has occurred. Please confirm connection to object storage.'
        else:
            message = f'Failed to connect external service: {param}'
            log_message = f'Storage service error has occurred. Failed to connect object storage.: {param}'
        Exception.__init__(self, message)
        self.code = 'InternalError'
        self.log_message = log_message


class MissingParameterError(Error):

    def __init__(self, param=''):
        if param == '':
            message = 'Missing parameter error occurred. Please confirm your request parameters.'
        else:
            message = f'Missing parameter error occurred. Please confirm your request parameters.: {param}'
        Exception.__init__(self, message)
        self.code = 'MissingParameterError'
        self.log_message = message


class InvalidParameterError(Error):

    def __init__(self, param='', raw=''):
        if param == '':
            message = 'Request parameter is invalid. Please confirm your request parameter.'
        else:
            message = f'Request parameter is invalid. Please confirm your request parameter [{param}:{raw}]'
        Exception.__init__(self, message)
        self.code = 'InvalidParameterError'
        self.log_message = message


class InvalidMethodError(Error):

    def __init__(self, method=''):
        if method == '':
            message = 'Request method is invalid. Please confirm request method.'
        else:
            message = f'Request method is invalid. Please confirm request method: {method}'
        Exception.__init__(self, message)
        self.code = 'InvalidMethodError'
        self.log_message = message


class InvalidURIError(Error):

    def __init__(self, uri):
        message = f'URI is invalid. Please confirm request endpoint: {uri}'
        Exception.__init__(self, message)
        self.code = 'InvalidURIError'
        self.log_message = message


class InvalidHeaderError(Error):

    def __init__(self, param=''):
        if param == '':
            message = 'Request headers are invalid. Please confirm your request header.'
        else:
            message = f'Request headers are invalid. Please confirm your request header: {param}'
        Exception.__init__(self, message)
        self.code = 'InvalidHeaderError'
        self.log_message = message


class InvalidDataError(Error):

    def __init__(self, data_name=''):
        if data_name == '':
            message = 'Failed to execute the process which is used user data source.'
        else:
            message = f'Failed to execute the process which is used user data source: {data_name}'
        Exception.__init__(self, message)
        self.code = 'InvalidDataError'
        self.log_message = message


class NotFoundError(Error):

    def __init__(self, param='', raw=''):
        if param == '':
            message = 'A resource with specified parameter has been not found.'
        else:
            message = f'A {param} with specified parameter = {raw} has been not found.'
        Exception.__init__(self, message)
        self.code = 'NotFoundError'
        self.log_message = message


class ProcessTimeoutError(Error):

    def __init__(self):
        message = 'Time out error occurred.'
        Exception.__init__(self, message)
        self.code = 'TimeoutError'
        self.log_message = message
