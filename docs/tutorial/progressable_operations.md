# Progressable Operations

Progressable operations are operations that can report their progress. 
This is useful for long-running operations (e.g., with multiple IO calls or numerous iterations).
To make an operation progressable, simply call the `progressable()` method on the operation.
Then, progress is reported using the `progress()` method.

## Progress Bar
By default, progressable operations also display a progress bar (powered by [tqdm](https://github.com/tqdm/tqdm)), 
which can be toggled on and off using the `with_pbar` flag (`Operation(...).progressable(with_pbar=False)`).

Nested progressable operations will display nested progress bars nicely, with no additional configuration:

![Nested progress bars](../assets/find_nth_prime.gif)

This is useful for CLI tools, for example.

For a CLI example, please refer to the [Find Nth Prime](https://github.com/oribarilan/oplog/blob/main/examples/prime_finder_demo/find_nth_prime.py) example.

## Completion Ratio

With or without progress bars, progressable operation maintain a `completion_ratio` property,
which can be access from the operation: `op.completion_ratio` (raises `AttributeError` if not progressable).

Completion ratio property is a float between 0 and 1, which represents the progress of the operation,
as reported by `iterations` argument and `op.progress()` call.
Completed operations will have a completion ratio of 1 (even if no `iterations` given).
In cases where completion ratio is unknown, it will be `None` 
(no iterations given and operation exited before completion - e.g., due to exception).
