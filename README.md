# oplog

An operational logging library for Python. No more cumbersome logging statements. No more investigating logs with complex regex. Just annotate your functions and let `oplog` do the rest.

Our most up-to-date documentation is available at [https://oribarilan.github.io/oplog/](https://oribarilan.github.io/oplog/).

## Concepts

Logs are often a mess. They are hard to read and hard to understand. They are often not actionable nor useful. There is a lack of consistency between logs. This makes it hard to understand what is going on in a system.

When investigating an issue, querying logs is often a pain. It is hard to find the relevant logs without being a regex master.

`oplog` aims to solve these problems by providing a simple, consistent and structured way to log operations.

Systems that use `oplog`, not only have a consistent way to log operations, but also have a consistent way to query them. This makes it to investigate issues, write alerts and build dashboards.

### Specifics

*Operation* is a unit of work that is performed. This is the smallest unit of work that can be logged. For example, a function call. Operations will automatically be logged when they are finished. Operations contain metadata (e.g. start time, end time, duration, etc.) as well as custom properties.

This is done by adding the *Operation* to the `LogRecord`, then allowing the users to handle it in a logging `Handler` and/or `Formatter`.

They can be printed nicely using a logging formatter (see `verbose_op_log_line_formatter.py` as an example).
In production systems, it is recommended to serialize the operations to JSON (see method `serialize()`) and send them to a log aggregation service such as [AzureDataExplorer](https://dataexplorer.azure.com/), [Elasticsearch](https://www.elastic.co/products/elasticsearch) or [Splunk](https://www.splunk.com/).

## Getting Started WIP

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

### Code Coverage

Code coverage is enforced by `pytest-cov`. To run the tests and generate a coverage report, 
run the following command from the root directory`:

```
pytest --cov=oplog --cov-report=xml oplog/tests
```

For VS Code, you can use [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) to view the coverage report within the editor.

## Deployment

Add additional notes about how to deploy this on a live system

## Documentation

Using mkdocs with mkdocs-material theme. To run the docs locally, run the following command from the root directory:

```
mkdocs serve
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors & Area Owners

* **Ori Bar-ilan**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

