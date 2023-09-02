# Development

## Environment Setup

This project was developed by the Author on MacOS, using VS Code as the IDE. The following instructions may vary depending on your environment.

1. Install the latest version of [Python](https://www.python.org/downloads/).
2. Install requirements by running `pip install -r requirements.txt` from the root directory.
3. Install dev requirements by running `pip install -r requirements-dev.txt` from the root directory.

Run `pytest` from the root directory to make sure everything is working.

## Code Coverage

Code coverage is enforced by `pytest-cov`. To run the tests and generate a coverage report, 
run the following command from the root directory`:

```
coverage run --omit 'oplog/tests/*','*/__pycache__/*' -m pytest
```

and then

```
coverage report -m
```

For VS Code, you can use [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) to view the coverage report within the editor.