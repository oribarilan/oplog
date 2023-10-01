from abc import ABC, abstractmethod


class OperationPropertyAlreadyExistsException(Exception):
    def __init__(self, op_name: str, prop_name: str) -> None:
        super().__init__(f'property `{prop_name}` already exists in op `{op_name}`')


class GlobalOperationPropertyAlreadyExistsException(Exception):
    def __init__(self, prop_name: str) -> None:
        super().__init__(f'global property `{prop_name}` already exists')


class LogRecordMissingOperationException(Exception):
    pass


class OpException(Exception, ABC):
    def __init__(self, op):
        super().__init__(f'operation `{op.name}` failed: {self.fail_reason()}')

    @abstractmethod
    def fail_reason(self) -> str:
        pass


class OperationIsAlreadyDisplayingException(OpException):
    def fail_reason(self) -> str:
        return 'operation is already displaying'
