import logging
from logging.config import dictConfig
from typing import Union

from fastapi import FastAPI

import os
import sys


# Get the parent directory of the current file (project_demo folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the repository root directory (one level up)
repository_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Add the repository root directory to the Python path
print("Adding repository root to Python path: {}".format(repository_root))
sys.path.append(repository_root)

from oplog.core.operated import Operated
from oplog.core.operation import Operation


logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger()


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    with Operation("read_item") as op:
        return {"item_id": item_id, "q": q}
