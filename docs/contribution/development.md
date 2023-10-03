# Development

## Environment Setup

This project was developed by the Author on MacOS, using VS Code as the IDE. The following instructions may vary depending on your environment.

1. Install the latest version of [Python](https://www.python.org/downloads/).
2. Install requirements by running `pip install -r requirements.txt` from the root directory.
3. Install dev requirements by running `pip install -r requirements-dev.txt` from the root directory.
4. Install [Just](https://github.com/casey/just#installation)

Run `just test` from the root directory to make sure everything is working.

## Development

We use `just` as our task runner. To see all available tasks, run `just --list`.
The main command you'll need is `just check`, which runs tests with coverage check, linting and code quality.
If this passes, your code will most likely pass the Pull-Request checks.

### Code Coverage

Code coverage is enforced by `coverage`. To run the tests and generate a coverage report, 
run the following command from the root directory`:

```
just test-coverage
```

We have a minimum coverage threshold of 90% of individual file coverage, and overall 95%.

### Code Linting

Linting is currently done using `ruff`. 

```
just lint
```

### Code Quality

Code quality currently runs just `mypy`.

```
just quality
```