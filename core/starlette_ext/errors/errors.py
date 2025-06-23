class AppError(Exception):
    status_code: 500
    message: str = 'Internal Server Error'

    def __init__(self, status_code: int, message: str, detail: str | None = None):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f'{self.status_code} {self.message}'


class ValidationError(AppError):
    status_code: 400
