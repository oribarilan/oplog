import logging

from oplog.operation import Operation


class CustomFormatter(logging.Formatter):
    def format(self, record) -> str:
        try:
            op = Operation.deserialize(record)
            return op.pretty_print()
        except:
            return record
