# Common Concepts

## Meta Properties (Operation metadata)

Meta properties are properties that describe the operation itself, such as the operation name, its duration, result (success / failure) etc.
They are managed automatically to every operation, and do not require additional care.

### Correlation ID

When investigating issues, developers find themselves needing to correlate between different operations. For example, when a user reports a bug, the developer will want to find all relevant log messages to help investigate and triage the bug. This is where `correlation_id` comes into play.

`correlation_id` is a special kind of meta property that is inherited by child operations from their parent operation, within the same execution thread. It can be used to correlate between all nested operations. These nested (or child) operations will have the same correlation ID as the root (or parent) operation.

The most common use case for `correlation_id` is for web server request handling. All operations that were executed within the same request, will be easily correlateable using the `correlation_id`.

``` py linenums="1" title="Correlation ID example"
def correlation_id_example():
    with Operation("root_op") as parent_op:
        with Operation("nested_op") as child_op:
            # here, child_op.correlation_id == parent_op.correlation_id
            # these operations will be easily correlateable in the logs
            pass
```

## Custom Properties

Custom properties are properties that are specific to the operation, and are not managed by the library. They are added using the `operation.add()` method (or similar).
Use custom properties to describe a specific instance of the operation.

For example, consider this method that fetches items from a storage, but first tries to fetch them from a cache:

``` py linenums="1" title="Item Fetching Example"
def fetch_items(self):
    items = self.cache.get('items')
    if items is None:
        items = self.storage.get('items')
        cache.set('items', items)
    return items
```

In this case, we might want to log the cache hit / miss, and the number of items returned. No more need for ambiguous log messages such as "items retrieved from cache" or "items retrieved from storage".

``` py linenums="1" title="Naive logging of cache hit / miss" hl_lines="3 7"
def fetch_items(self):
    items = self.cache.get('items')
    source = 'cache' if items is not None else 'storage'
    if items is None:
        items = self.storage.get('items')
        cache.set('items', items)
    self.log(f'{len(items_count)} items retrieved from {source}')
    return items
```

``` title="Output Example"
2023-08-09 22:03:31.243611 [INFO]: 3 items retrieved from cache
```

``` py linenums="1" title="Doing it the oplog way" hl_lines="2 5 9"
def fetch_items(self):
    with Operation(name="foo.get_items_from_storage") as op:
        items = self.cache.get('items')
        is_cache_hit = items is not None
        op.add('is_cache_hit', is_cache_hit)
        if not is_cache_hit:
            items = self.storage.get('items')
            cache.set('items', items)
        op.add('items_count', len(items))
    return items
```

``` title="Output Example"
2023-08-09 22:03:31.243611 (0ms): [foo.get_items_from_storage / Success] {'is_cache_hit': True, 'items_count': 3}
```

At a first glance, the common log-book style seems easier to read, however, it is not scalable. As the number of operations grows, the number of log messages grows as well, and it becomes harder to find the relevant log message.
Developers and analysts will have to either read through many messages that are text-heavy, or, when scaled, will have to extract information from each specific log line (regex, anyone?).

Oplog solves this problem by providing a structured way to log operations, and by providing a way to filter and query the log messages. You can still use them to structure a nice log-book if you wish (see `VerboseOpLogLineFormatter`), but they provide much more flexibility and scalability.

## Global Properties

Global properties are properties that are meant to be set once, and will then be available across all operations in the program lifetime.
Use `operation.add_global()` to add a global property.

``` py linenums="1" hl_lines="8 9"
import logging
from oplog import Operated, Operation
from oplog.formatters import VerboseOplogLineFormatter

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logging.getLogger().handlers[0].setFormatter(VerboseOplogLineFormatter())

Operation.add_global('project_version', '1.3.0')
Operation.add_global('build_version', '20230120_001')

@Operated()
def foo():
    pass

foo()
```
    
``` title="Output"
2023-08-31 22:01:26.458748 (0ms): [foo.foo / Success] {'project_version': '1.3.0', 'build_version': '20230120_001'}
```