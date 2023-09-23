# Examples

🚧 Work in progress. Please come back later. 🚧

## Fluent Calculator

This demo shows how to use oplog for structured logging. The most common benefit of structured logs is the ability to query them in a performant way, as well as creating dashboards and monitors on top of them. Usually, this is achieved by ingesting the logs into a columnar database, such as [AWS CloudWatch](https://aws.amazon.com/cloudwatch/), [Google BigQuery](https://cloud.google.com/bigquery), [Azure Data Explorer](https://azure.microsoft.com/en-us/products/data-explorer), [Splunk](https://www.splunk.com/) and more.

In these cases, we create JSON object out of every oplog, and ingest it into the database.
In the Fluent Calculator example, we demonstrate the same concept but using CSV instead of JSON, for readability purposes.

Running the example, will create the following CSV log file:

| StartTime          | DurationMS | OperationName        | CorrelationId                  | Result  | ExceptionType    |
|------------------- |------------|---------------------- |------------------------------- |---------|------------------ |
| 11/08/2023  22:28:24.0 | 0      | FluentCalculator.__init__ | 04a94ba0-ed7d-458a-94f5-0f1dd033fcbd | Success | None            |
| 11/08/2023  22:28:24.0 | 1000   | FluentCalculator.add  | 04a94ba0-ed7d-458a-94f5-0f1dd033fcbd | Success | None            |
| 11/08/2023  22:28:25.0 | 1000   | FluentCalculator.subtract | 04a94ba0-ed7d-458a-94f5-0f1dd033fcbd | Success | None            |
| 11/08/2023  22:28:26.0 | 1003   | FluentCalculator.get_result | 04a94ba0-ed7d-458a-94f5-0f1dd033fcbd | Success | None            |
| 11/08/2023  22:28:24.0 | 3007   | first_calc           | 04a94ba0-ed7d-458a-94f5-0f1dd033fcbd | Success | None            |
| 11/08/2023  22:28:27.0 | 0      | FluentCalculator.__init__ | e3305e32-9d79-4ca4-99c2-36af2a905d0e | Success | None            |
| 11/08/2023  22:28:27.0 | 1004   | FluentCalculator.add  | e3305e32-9d79-4ca4-99c2-36af2a905d0e | Success | None            |
| 11/08/2023  22:28:28.0 | 1002   | FluentCalculator.divide | e3305e32-9d79-4ca4-99c2-36af2a905d0e | Failure | ZeroDivisionError |
| 11/08/2023  22:28:27.0 | 2008   | second_calc          | e3305e32-9d79-4ca4-99c2-36af2a905d0e | Failure | ZeroDivisionError |

Things to note (and love ❤️) about this log file:

1. **Readable**: It is human readable, yet, without cumbersome text.
2. **Scalable**: It fits into columnar databases like a glove.
3. **Production Ready**: It is easy to query, analyze and monitor, for production scenarios.
4. **Easy for Devs**: Note the two different correlation IDs, one per calculation. We can correlate all operations that were executed within the failing calculation, for example. Powerful for debugging and investigations.

And much more...

## Server Demo

Our basic server demo is a simple web server that serves...
It is written in [FastAPI](https://github.com/tiangolo/fastapi).

Install the dependencies by navigating into the `examples/server_demo` directory and running:

```bash
pip install -r requirements.txt
```

Then, run the server with:

```bash
uvicorn main:app --reload
```