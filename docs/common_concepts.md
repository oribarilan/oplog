# Common Concepts

## Meta properties

## Custom Properties

## Global Properties

Global properties are properties that are meant to set once, and will then be available across all operations.
Use `operation.add_global()` to add a global property.

``` py linenums="1" hl_lines="7 8"
import logging
from oplog.core import Operation, VerboseOpLogLineFormatter

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logging.getLogger().handlers[0].setFormatter(VerboseOpLogLineFormatter())

Operation.add_global('project_version', '1.3.0')
Operation.add_global('build_version', '20230120_001')

@Operation()
def foo():
    pass
```
    
``` bash title="Output"
2023-08-09 22:03:31.243611 (0ms): [foo.foo / Success] {'project_version': '1.3.0', 'build_version': '20230120_001'}
```