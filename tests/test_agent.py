import unittest
import os
import json
from unittest.mock import patch, MagicMock

# This is a bit of a hack to import the agent script
# as it's not a proper module.
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import agent

class TestAgentCore(unittest.TestCase):

    def setUp(self):
        """Set up a controlled environment for each test."""
        self.COMMANDS = agent.COMMANDS
        # Mock the logger to prevent it from writing to console/file during tests
        self.patcher = patch('agent.LOGGER', new=MagicMock())
        self.mock_logger = self.patcher.start()

    def tearDown(self):
        """Clean up after each test."""
        self.patcher.stop()

    def test_normalize_and_validate_valid_standard_command(self):
        """Test a valid command with the standard '{command, params}' format."""
        data = {"command": "message", "params": {"text": "hello"}}
        result = agent.normalize_and_validate_command(data)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "message")
        self.assertEqual(result[1], {"text": "hello"})

    def test_normalize_and_validate_valid_legacy_command(self):
        """Test a valid command with the backward-compatible flat format."""
        data = {"command": "message", "text": "hello legacy"}
        result = agent.normalize_and_validate_command(data)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "message")
        self.assertEqual(result[1], {"text": "hello legacy"})

    def test_normalize_and_validate_unknown_command(self):
        """Test that an unknown command is rejected."""
        data = {"command": "non_existent_command", "params": {}}
        result = agent.normalize_and_validate_command(data)
        self.assertIsNone(result)
        self.mock_logger.warning.assert_called_with("Unknown/forbidden command received: 'non_existent_command'")

    def test_normalize_and_validate_missing_command_key(self):
        """Test that a dictionary without a 'command' key is rejected."""
        data = {"params": {"text": "some text"}}
        result = agent.normalize_and_validate_command(data)
        self.assertIsNone(result)
        self.mock_logger.warning.assert_called_with("Command file is missing 'command' key.")

    def test_normalize_and_validate_empty_dict(self):
        """Test that an empty dictionary is rejected."""
        data = {}
        result = agent.normalize_and_validate_command(data)
        self.assertIsNone(result)

    def test_normalize_and_validate_invalid_params_type(self):
        """Test that a command with non-dict params is rejected."""
        data = {"command": "message", "params": "not-a-dict"}
        result = agent.normalize_and_validate_command(data)
        self.assertIsNone(result)
        self.mock_logger.warning.assert_called_with("Command 'message' has invalid 'params'. Expected a dictionary.")

    @patch.dict(agent.COMMANDS, {'delete_file': MagicMock()})
    def test_dispatch_command_success(self):
        """Test that a valid command is dispatched correctly."""
        params = {"path": "/test.txt", "confirm": True}
        agent.dispatch_command("delete_file", params)
        agent.COMMANDS['delete_file'].assert_called_once_with(**params)
        self.mock_logger.info.assert_any_call("Successfully executed command: 'delete_file'")

    def test_dispatch_command_exception(self):
        """Test that exceptions during command execution are caught and logged."""
        # We test a command that will raise a TypeError because of mismatched params
        params = {"path": "/test.txt", "wrong_param": "should cause error"}
        agent.dispatch_command("delete_file", params)
        self.mock_logger.error.assert_called_once()
        # Get the first call's arguments
        call_args, _ = self.mock_logger.error.call_args
        # The first argument of the call is the log message
        log_message = call_args[0]
        self.assertIn("Mismatched parameters for command 'delete_file'", log_message)
        self.assertIn("got an unexpected keyword argument 'wrong_param'", log_message)

class TestDeleteFileSafety(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('agent.LOGGER', new=MagicMock())
        self.mock_logger = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @patch('os.path.exists', return_value=True)
    @patch('os.remove')
    def test_delete_file_with_confirm_true(self, mock_remove, mock_exists):
        """Test that delete_file proceeds when confirm=True."""
        agent.delete_file(path="dummy.txt", confirm=True)
        mock_exists.assert_called_once_with("dummy.txt")
        mock_remove.assert_called_once_with("dummy.txt")
        self.mock_logger.info.assert_called_with("Successfully deleted file: dummy.txt")

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_file_with_confirm_false(self, mock_remove, mock_exists):
        """Test that delete_file is skipped when confirm=False."""
        agent.delete_file(path="dummy.txt", confirm=False)
        mock_exists.assert_not_called()
        mock_remove.assert_not_called()
        self.mock_logger.warning.assert_called_with("delete_file called without confirm=True for 'dummy.txt'. Skipping.")

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_file_with_confirm_missing(self, mock_remove, mock_exists):
        """Test that delete_file is skipped when confirm is missing."""
        agent.delete_file(path="dummy.txt")
        mock_exists.assert_not_called()
        mock_remove.assert_not_called()
        self.mock_logger.warning.assert_called_with("delete_file called without confirm=True for 'dummy.txt'. Skipping.")

    @patch('os.path.exists', return_value=False)
    @patch('os.remove')
    def test_delete_file_nonexistent_file(self, mock_remove, mock_exists):
        """Test that delete_file handles non-existent files gracefully."""
        agent.delete_file(path="nonexistent.txt", confirm=True)
        mock_exists.assert_called_once_with("nonexistent.txt")
        mock_remove.assert_not_called()
        self.mock_logger.warning.assert_called_with("File not found for deletion: nonexistent.txt")

if __name__ == '__main__':
    unittest.main()
