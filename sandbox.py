import os
import sys

# Mocking library behavior
repository_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(repository_root)

import logging
from oplog.core.operation import Operation
from oplog.core.operated import Operated
from oplog.formatters.verbose_oplog_line_formatter import VerboseOplogLineFormatter

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logging.getLogger().handlers[0].setFormatter(VerboseOplogLineFormatter())

Operation.add_global('project_version', '1.3.0')
Operation.add_global('build_version', '20230120_001')

@Operated()
def foo():
    pass

foo()