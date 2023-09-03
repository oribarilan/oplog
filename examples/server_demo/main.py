# This example shows how to use oplog package with FastAPI.
# The get API endpoint is decorated with @Operated, which means that every request 
# will be logged as an operation.
# All subsequent operations will correlated to that operation using the correlation_id.
# To run this example, run the following command from the repository root directory:
# uvicorn examples.server_demo.main:app --reload

import logging

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

from oplog import Operation, Operated, OperationHandler # noqa: E402
from oplog.formatters import VerboseOplogLineFormatter # noqa: E402

stream_op_handler = OperationHandler(
    handler=logging.StreamHandler(), # <-- any logging handler
    formatter=VerboseOplogLineFormatter(), # <-- custom formatter or built-in ones
)
logging.basicConfig(level=logging.INFO, handlers=[stream_op_handler])

app = FastAPI()

@app.get("/")
async def read_root():
    with Operation("root"):
        return { "Hello": compute_response() }

@Operated()
def compute_response():
    return "World"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
