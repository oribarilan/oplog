# Operation

Operations are the core of the library. 
They are used to wrap code blocks, and provide a unified way to log and trace them, with rich context.

## Basic Usage

The most basic usage of an operation is to wrap a code block with a `with` statement:

``` py linenums="1" title="Basic Usage"
with Operation(name="foo") as op:
    # do something
    pass
```

This will fire a log record with rich operation metadata, like duration, result, exception, thread name, etc.
This operation can be formatted according to your needs (verbose log line, csv, JSON, etc.).    

For reference on example formatters, refer to 
[OplogCsvFormatter](https://github.com/oribarilan/oplog/blob/main/oplog/formatters/oplog_csv_formatter.py) 
or [VerboseOplgLineFormatter](https://github.com/oribarilan/oplog/blob/main/oplog/formatters/verbose_oplog_line_formatter.py).

A complete example that will print the operation log record to the stdout, using the verbose formatter:

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
        pass
    
bar()
```
