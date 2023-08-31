# Getting Started

## Installation
You can install oplog from PyPI using pip:
```bash
pip install op-log
```

## First Steps

### Setting up the logger

Oplog naturally extends Python's built-in logger. 
To start, add an "Operation handler" of your choice, by creating any Python logging handler and attaching `OperationLogFilter` to it. Then, customize your output log format with `VerboseOpLogLineFormatter` or create your own formatter.

``` py linenums="1" title="Setting up the logger" hl_lines="6 7"
import logging
from oplog import Operated, OperationLogFilter
from oplog.formatters import VerboseOplogLineFormatter

stream_op_handler = logging.StreamHandler()
stream_op_handler.addFilter(OperationLogFilter()) # <-- Only handle operation logs
stream_op_handler.setFormatter(VerboseOplogLineFormatter()) # <-- Example on how to use a custom formatter
logging.basicConfig(level=logging.INFO, handlers=[stream_op_handler])

# using a decorator, for simplicity
@Operated()
def foo():
    pass
    
foo()
```

``` title="Output"
2023-08-31 17:31:08.519900 (0ms): [foo.foo / Success]
```

As you can see, you can use any handler, formatter and filter you want. Oplog does not interfere with them.

* Line 6 (highlighted) makes any handler an "Operation Handler". If you want to also handle log-book-style logs, you can keep your existing handler (for log message, like `logger.info("This is a conventional log message")`).
* Line 7 (highlighted) decides on the log format. It is using a built-in formatter, but you can create your own formatter easily.

### Using Context Managers

For more control, you can use the context manager syntax. This allows, for example, to add custom properties to the operation.

``` py linenums="1" title="Logging operations using the context manager" hl_lines="12 13"
import logging
from oplog import Operation, OperationLogFilter
from oplog.formatters import VerboseOplogLineFormatter

stream_op_handler = logging.StreamHandler()
stream_op_handler.addFilter(OperationLogFilter()) # <-- Only handle operation logs
stream_op_handler.setFormatter(VerboseOplogLineFormatter()) # <-- Example on how to use a custom formatter
logging.basicConfig(level=logging.INFO, handlers=[stream_op_handler])

# using a context manager, for more control
def bar():
    with Operation(name="my_operation") as op:
        op.add("metric", 5)
        pass
    
bar()
```

``` title="Output"
2023-08-31 17:41:09.088966 (0ms): [my_operation / Success] {'metric': 5}
```
