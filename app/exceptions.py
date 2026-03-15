class AppError(Exception):
    status_code = 500
    code = 'app_error'

    def __init__(self, message, *, code=None, status_code=None):
        super().__init__(message)
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code


class BusinessRuleError(AppError):
    status_code = 409
    code = 'business_rule'


class ValidationError(AppError):
    status_code = 400
    code = 'validation_error'


class PermissionDenied(AppError):
    status_code = 403
    code = 'forbidden'


class NotFound(AppError):
    status_code = 404
    code = 'not_found'
