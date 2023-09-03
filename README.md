<!-- Top Section -->
<p align="center">
  <a href="https://oribarilan.github.io/oplog"><img src="https://oribarilan.github.io/oplog/imgs/logo_full.png" alt="oplog logo"></a>
</p>

<p align="center">
  <b>Modern logging library for Python applications.</b>
</p>

<!-- Badges using https://shields.io/badges/ -->
<p align="center">
  <!-- Python versions -->
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11-blue" alt="python versions">
  </a>
  <!-- Downloads -->
  <a href="https://pypi.org/project/op-log/">
    <img src="https://img.shields.io/pypi/dm/op-log?link=https%3A%2F%2Fpypi.org%2Fproject%2Fop-log%2F" alt="downloads">
  </a>
  <!-- Ruff credit -->
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <!-- Build -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/package_build.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/package_build.yml" alt="build">
  </a>
  <!-- Lint -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/lint.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/lint.yml?label=lint" alt="lint">
  </a>
  <!-- Coverage -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/coverage.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/coverage.yml?label=coverage%3E95%25" alt="coverage">
  </a>
  <!-- Security -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/security_check.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/security_check.yml?label=security" alt="security">
  </a>
</p>

<hr>

Full documentation: [oribarilan.github.io/oplog](https://oribarilan.github.io/oplog/).

Source code: [github.com/oribarilan/oplog](http://www.github.com/oribarilan/oplog/).

---

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

oplog naturally extends Python's built-in logger. 
To start, create an `OperationHandler`, and attach to it any  logging handler of your choice. Additionally, you should customize your output log format with a formatter. You can create your own or use a built-in one (such as  `VerboseOpLogLineFormatter`).

``` py linenums="1" title="Setting up the logger" hl_lines="5 6 7 8"
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

``` py linenums="1" title="Logging operations using the context manager" hl_lines="13 1"
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
