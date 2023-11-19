class WinAPIError(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
        message = 'Windows api error, error_code: {}'.format(self.error_code)
        super(WinAPIError, self).__init__(message)


class PymemError(Exception):
    def __init__(self, message):
        super(PymemError, self).__init__(message)


class ProcessError(PymemError):
    def __init__(self, message):
        super(ProcessError, self).__init__(message)


class ProcessNotFound(ProcessError):
    def __init__(self, process_name):
        message = 'Could not find process: {}'.format(process_name)
        super(ProcessNotFound, self).__init__(message)


class CouldNotOpenProcess(ProcessError):
    def __init__(self, process_id):
        message = 'Could not open process: {}'.format(process_id)
        super(CouldNotOpenProcess, self).__init__(message)


class PymemMemoryError(PymemError):
    def __init__(self, message):
        super(PymemMemoryError, self).__init__(message)


class MemoryReadError(PymemMemoryError):
    def __init__(self, address, length, error_code=None):
        message = 'Could not read memory at: {}, length: {}'.format(address, length)
        if error_code:
            message += ' - GetLastError: {}'.format(error_code)
        super(MemoryReadError, self).__init__(message)


class MemoryWriteError(PymemMemoryError):
    def __init__(self, address, value, error_code=None):
        message = 'Could not write memory at: {}, length: {}'.format(address, value)
        if error_code:
            message += ' - GetLastError: {}'.format(error_code)
        super(MemoryWriteError, self).__init__(message)


class PymemAlignmentError(PymemError):
    def __init__(self, message):
        super(PymemAlignmentError, self).__init__(message)


class PymemTypeError(PymemError):
    def __init__(self, message):
        super(PymemTypeError, self).__init__(message)
