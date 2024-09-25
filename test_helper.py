import unittest
import os
import asyncio
from helper import Helper

class TestHelper(unittest.TestCase):
    def setUp(self):
        """Set up a temporary environment for testing."""
        self.script_path = 'test_script.py'
        self.test_file = 'test_script_temp.py'
        self.log_widget = MockLogWidget()  # Mock the log widget for testing
        self.helper = Helper(self.script_path, self.test_file, self.log_widget)

        # Create a sample script for testing
        with open(self.script_path, 'w') as f:
            f.write("# === Start Editable Section ===\n")
            f.write("def existing_function():\n")
            f.write("    print('Hello, World!')\n")
            f.write("# === End Editable Section ===\n")

    def tearDown(self):
        """Clean up any files created during testing."""
        if os.path.exists(self.script_path):
            os.remove(self.script_path)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_suggest_new_code(self):
        """Test if suggest_new_code generates suggestions correctly."""
        new_code = self.helper.suggest_new_code()
        self.assertIn("def new_helper_function", new_code)
        self.assertIn("# TODO: Add logic to assist existing functions.", new_code)

    async def test_inject_code_async(self):
        """Test if code injection works as expected."""
        new_code = "print('New code injected!')"
        await self.helper.inject_code_async(new_code)

        # Check if the test script was created and contains the new code
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn("New code injected!", content)

class MockLogWidget:
    """A simple mock for the log widget to capture log messages."""
    def __init__(self):
        self.messages = []

    def insert(self, index, message):
        self.messages.append(message)

    def see(self, index):
        pass

if __name__ == '__main__':
    unittest.main()
