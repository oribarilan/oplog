# Getting Started

## Installation
You can install oplog from PyPI using pip:
```bash
pip install oplog
```

## First Steps

### Setting up the logger

You already have a logger in your code. Oplog does not interfere with it, but works with it.
Set up an additional handler, and set the formatter to `OpLogLineFormatter`:

``` py linenums="1" title="Setting up the logger" hl_lines="3"

# logger setup
stream_op_handler = logging.StreamHandler()
stream_op_handler.addFilter(OperationLogFilter()) # <-- Only handle operation logs
stream_op_handler.setFormatter(VerboseOpLogLineFormatter()) # <-- Example on how to use a custom formatter
logging.basicConfig(level=logging.INFO, handlers=[stream_op_handler])

# using decorators, for simplicity
@Operated()
def foo():
    pass

# using context manager, for more control
def bar():
    with Operation() as op:
        op.add("metric", 5)
        pass
```

``` title="Output"
2023-08-09 22:03:31.243611 (0ms): [foo.foo / Success]
2023-08-09 22:03:31.356331 (0ms): [bar.bar / Success] {'metric': 5}
```

As you can see, you can use any handler, formatter and filter you want. Oplog does not interfere with them.
However, line #2 (highlighted) is important. It makes the handler only handle operation logs. You can have another handler if you want to handle other logs (for log message, like `logger.info("This is a conventional log message")`).