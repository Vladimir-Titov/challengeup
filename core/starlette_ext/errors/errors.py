class AppError(Exception):
    status_code: int = 500
    message: str = 'Internal Server Error'

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f'{self.status_code} {self.message}'


class ValidationError(AppError):
    status_code: int = 400
