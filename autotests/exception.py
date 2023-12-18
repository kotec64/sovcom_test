from logging import Logger


class InvalidExpectedConditions(BaseException):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class InvalidSelectType(BaseException):
    def __init__(self, message: str):
        self.message = message
    def __str__(self) -> str:
        return self.message


class RedirectionFailedException(BaseException):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class TimeOutElementNotFoundException(BaseException):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class UnexpectedBehaviorException(BaseException):
    def __init__(self, message: str, logger: Logger):
        self.message = message
        logger.critical(self.message)

    def __str__(self) -> str:
        return self.message


class NoSuchOptionInTheListException(BaseException):
    def __init__(self, message: str, logger: Logger):
        self.message = message
        logger.critical(self.message)

    def __str__(self) -> str:
        return self.message


class UnexpectedElementTextException(BaseException):
    def __init__(self, message: str, logger: Logger):
        self.message = message
        logger.critical(message)

    def __str__(self) -> str:
        return self.message


class UnexpectedAttributeTextException(BaseException):
    def __init__(self, message: str, logger: Logger):
        self.message = message
        logger.critical(message)

    def __str__(self) -> str:
        return self.message


class WrongArgumentUsageException(BaseException):
    def __init__(self, message: str, logger: Logger):
        self.message = f"Wrong argument usage. {message}"
        logger.critical(self.message)

    def __str__(self) -> str:
        return self.message
