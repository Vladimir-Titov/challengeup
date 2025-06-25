class AppError(Exception):
    status_code: int = 500
    message: str = 'Internal Server Error'

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f'{self.status_code} {self.message}'

    @classmethod
    def code(cls) -> str:
        return ''.join(['_' + i.lower() if i.isupper() else i for i in cls.__name__]).lstrip('_')


class ValidationError(AppError):
    status_code: int = 400


class MethodNotAllowedError(AppError):
    status_code: int = 405
    message: str = 'Method Not Allowed'
