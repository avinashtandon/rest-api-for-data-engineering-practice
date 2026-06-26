from typing import Optional

class APIException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message

class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, code="NOT_FOUND", message=message)

class BadRequestException(APIException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=400, code="BAD_REQUEST", message=message)

class UnauthorizedException(APIException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=401, code="UNAUTHORIZED", message=message)

class ForbiddenException(APIException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(status_code=403, code="FORBIDDEN", message=message)
