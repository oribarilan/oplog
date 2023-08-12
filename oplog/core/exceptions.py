class OperationPropertyAlreadyExistsException(Exception):
    def __init__(self, op_name: str, prop_name: str) -> None:
        super().__init__(f'property `{prop_name}` already exists in op `{op_name}`')