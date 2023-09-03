# Getting Started

## Installation
You can install oplog from PyPI using pip:
```bash
pip install op-log
```

## First Steps

### Setting up the logger

oplog naturally extends Python's built-in logger. 
To start, create an `OperationHandler`, and attach to it any  logging handler of your choice. Additionally, you should customize your output log format with a formatter. You can create your own or use a built-in one (such as  `VerboseOpLogLineFormatter`).

``` py linenums="1" title="Setting up the logger" hl_lines="5 6 7 8 12"
import logging
from oplog import Operated, OperationHandler
from oplog.formatters import VerboseOplogLineFormatter

stream_op_handler = OperationHandler(
    handler=logging.StreamHandler(), # <-- any logging handler
    formatter=VerboseOplogLineFormatter(), # <-- custom formatter or built-in ones
)   
logging.basicConfig(level=logging.INFO, handlers=[stream_op_handler])

# using a decorator, for simplicity
@Operated()
def foo():
    pass
    
foo()
```

Output:
``` title="Output"
2023-08-31 17:31:08.519900 (0ms): [foo.foo / Success]
```

As you can see, you can use any handler, formatter and filter you want. Oplog does not interfere with them.

* Line 6 (highlighted) makes any handler an "Operation Handler". If you want to also handle log-book-style logs, you can keep your existing handler (for log message, like `logger.info("This is a conventional log message")`).
* Line 7 (highlighted) decides on the log format. It is using a built-in formatter, but you can create your own formatter easily.

### Using Context Managers

For more control, you can use the context manager syntax. This allows, for example, to add custom properties to the operation.

``` py linenums="1" title="Logging operations using the context manager" hl_lines="13 14"
import logging
from oplog import Operation, OperationHandler
from oplog.formatters import VerboseOplogLineFormatter

stream_op_handler = OperationHandler(
    handler=logging.StreamHandler(), # <-- any logging handler
    formatter=VerboseOplogLineFormatter(), # <-- custom formatter or built-in ones
)   
logging.basicConfig(level=logging.INFO, handlers=[stream_op_handler])

# using a context manager, for more control
def bar():
    with Operation(name="my_operation") as op:
        op.add("metric", 5)
        pass
    
bar()
```

Output:
``` title="Output"
2023-08-31 17:41:09.088966 (0ms): [my_operation / Success] {'metric': 5}
```
