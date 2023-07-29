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
print("Adding repository root to Python path: {}".format(repository_root))
sys.path.append(repository_root)

from oplog.core.operated import Operated
from oplog.core.operation import Operation
from oplog.formatters.verbose_op_log_line_formatter import VerboseOpLogLineFormatter
from oplog.core.operation_logger import OperationLogFilter

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.addFilter(OperationLogFilter())
stream_handler.setFormatter(VerboseOpLogLineFormatter())
logger.addHandler(stream_handler)
logger.addHandler(logging.StreamHandler())
logger.info("test")

# oplog_stream_handler = OpLogStreamHandler(formatter=VerboseOpLogLineFormatter())
# logger.addHandler(oplog_stream_handler)

# oplog_file_handler = OpLogFileHandler(filename="oplog.log")
# logger.addHandler(oplog_file_handler)


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    with Operation("read_item") as op:
        return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
