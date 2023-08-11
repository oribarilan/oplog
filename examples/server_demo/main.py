import logging
from logging.config import dictConfig
from typing import Union

from fastapi import FastAPI

import os
import sys

import uvicorn


# Get the parent directory of the current file (project_demo folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the repository root directory (one level up)
repository_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Add the repository root directory to the Python path
sys.path.append(repository_root)

from oplog.core.operated import Operated
from oplog.core.operation import Operation
from oplog.formatters.verbose_oplog_line_formatter import VerboseOplogLineFormatter
from oplog.core.operation_log_filter import OperationLogFilter

stream_op_handler = logging.StreamHandler()
stream_op_handler.addFilter(OperationLogFilter()) # <-- Only handle operation logs
stream_op_handler.setFormatter(VerboseOplogLineFormatter()) # <-- Example on how to use a custom formatter
logging.basicConfig(level=logging.INFO, handlers=[stream_op_handler])

app = FastAPI()


@app.get("/")
async def read_root():
    with Operation("read_root") as op:
        return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
