# oplog

![oplog logo](https://oribarilan.github.io/oplog/imgs/logo_full.png)

## Installation
You can install oplog from PyPI using pip:
```bash
pip install op-log
```

## What is oplog?

oplog is a modern logging library for Python application.
oplog offers a different paradigm for logging, which is based on the concept of logging operations.
Instead of creating a "log-book", which is a long scroll of text messages, oplog is about logging operations with rich data.

Please refer to our full documentation at [oribarilan.github.io/oplog](https://oribarilan.github.io/oplog/).

### Key features

1. **Object Oriented**: Intuitive API, easy to use and extend.
2. **Modern & Scalable**: Unlike log messages, oplog is scaleable. Ingesting oplogs to a columnar database allows you to query, analyze and monitor your app in a modern and performant way.
3. **Standardized**: No more mess and inconsistency across your logs. oplog creates a standard for how logs should be written across your code base. Clean code, clean logs.
4. **Production Ready**: Easily create dashboards and monitors on top of logged data.
5. **Lightweight**: oplog is a layer on top of the standard Python logging library. It is easy to integrate and use.
6. **Minimal**: While oplog is rich with metadata, you only log what you need. Creating smaller and more efficient logs.

## Getting Started

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

Output:
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

Output:
``` title="Output"
2023-08-31 17:41:09.088966 (0ms): [my_operation / Success] {'metric': 5}
```
