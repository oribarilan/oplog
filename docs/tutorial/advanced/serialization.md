# Operation Serialization

!!! note

    In most cases custom serialization is not required. Try using a custom formatter, or the default serialization. 

While the recommended way to format operation logs is to implement a `oplog.formatters.OperationFormatter` formatter,
in some scenarios, a formatter may not be available for the developer.
In such cases, it is common for tools/libs to use the `str` representation of the operation (`%(oplog)s`).
So, `oplog` supports this behavior out-of-the-box.

A common example is `pytest`. 
`pytest` uses the `str` representation of the operation to display the operation in the terminal,
most commonly used to display errors (and warning) during tests.

Although this is supported, developers may want to override the default string serialization of operations.
`pytest` has limited formatting options (read more about it in [pytest: How to manage logging](https://docs.pytest.org/en/7.1.x/how-to/logging.html).
so `oplog` provides a way to override the default string serialization of operations.

This is done in the `config` class method, which is commonly called once during logger setup. 

## Example

```python
Operation.config(..., serializer=lambda op: f"{op.name} - {op.status}")
```

You can read more about `config` in [Config](../config.md).