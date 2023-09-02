from functools import update_wrapper
from typing import Optional
from oplog.operation import Operation


class Operated:
    def __init__(self, name: Optional[str] = None, suppress: bool = False):
        """Creates an underlying operation. Refer to Operation for more details.
        This should be used as a decorator on a function or method.
        For arguments documentation, refer to Operation.__init__.
        """
        self.name = name
        self.suppress = suppress

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.name is not None:
                op_name = self.name
            else:
                function_name = func.__name__
                try:
                    # get class name if possible
                    qualifier_name = func.__qualname__.split(".")[0]
                except AttributeError:
                    # otherwise, get module name
                    qualifier_name = func.__module__

                op_name = f"{qualifier_name}.{function_name}"
                
            with Operation(name=op_name, suppress=self.suppress):
                result = func(*args, **kwargs)

            return result

        update_wrapper(wrapper, func)
        return wrapper
