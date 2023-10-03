default:
    just --list


alias tc := test-coverage
alias t := test
alias c := check

# execute tests with coverage
test-coverage:
    coverage run --omit 'oplog/tests/*','*/__pycache__/*','examples' -m pytest --ignore=examples
    coverage report -m --fail-under=95

# execute tests
test:
    pytest --ignore=examples

# execute linting utils
lint:
    ruff .

# execute quality utils
quality:
    mypy .

# execute all code checks (linting and quality)
check:
    just lint
    just quality
    just test-coverage

# build and run docs
docs:
    mkdocs serve