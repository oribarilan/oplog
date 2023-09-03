import logging
from unittest import mock
from oplog import OperationHandler
from oplog.operation import Operation
from oplog.tests.logged_test_case import OpLogTestCase


class TestOperationHandler(OpLogTestCase):
    def test_operationHandler_loggingOperation_operationLogged(self):
        handler = OperationHandler(logging.StreamHandler())
        logging.getLogger().addHandler(handler)
        
        with Operation(name="test_op") as op:
            pass
        
        self.assertEqual(self.get_op("test_op"), op)
        
    def test_operationHandler_loggingOperationAndInfo_infoNotLoggedByHandler(self):
        handler_mock = mock.Mock()
        op_handler = OperationHandler(handler_mock)
        logging.getLogger().addHandler(op_handler)
        
        with Operation(name="test_op") as op:
            pass
            logging.getLogger().info("test_info")
        
        # assert called once    
        self.assertEqual(len(handler_mock.emit.call_args_list), 1)
        
        # assert called once with a log record with op
        call_args = handler_mock.emit.call_args_list[0][0]
        self.assertEqual(call_args[0].oplog, op)

    def test_operationHandler_loggingInfo_infoNotLoggedByHandler(self):
        handler_mock = mock.Mock()
        op_handler = OperationHandler(handler_mock)
        logging.getLogger().addHandler(op_handler)
        
        logging.getLogger().info("test_info")
        
        # assert called once    
        handler_mock.emit.assert_not_called()
