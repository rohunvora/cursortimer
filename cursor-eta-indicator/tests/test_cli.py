"""Unit tests for CLI functionality."""

import unittest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

from cursor_eta.__main__ import main, demo_task


class TestCLI(unittest.TestCase):
    """Test the command-line interface."""
    
    def test_demo_task_simple(self):
        """Test demo task with simple complexity."""
        with patch('builtins.print') as mock_print:
            result = demo_task("Test Task", "simple")
            
        self.assertEqual(result, "✅ Completed Test Task successfully!")
        
        # Check that appropriate messages were printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("Test Task" in call for call in print_calls))
        self.assertTrue(any("simple" in call for call in print_calls))
        
    def test_demo_task_medium(self):
        """Test demo task with medium complexity."""
        with patch('time.sleep'):  # Speed up test
            result = demo_task("Medium Task", "medium")
            
        self.assertEqual(result, "✅ Completed Medium Task successfully!")
        
    def test_demo_task_complex(self):
        """Test demo task with complex complexity."""
        with patch('time.sleep'):  # Speed up test
            result = demo_task("Complex Task", "complex")
            
        self.assertEqual(result, "✅ Completed Complex Task successfully!")
        
    @patch('sys.argv', ['cursor-eta', '--version'])
    def test_version_flag(self):
        """Test --version flag."""
        with self.assertRaises(SystemExit) as cm:
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main()
                
        self.assertEqual(cm.exception.code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("0.1.0", output)
        
    @patch('sys.argv', ['cursor-eta', '--help'])
    def test_help_flag(self):
        """Test --help flag."""
        with self.assertRaises(SystemExit) as cm:
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main()
                
        self.assertEqual(cm.exception.code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("cursor-eta", output)
        self.assertIn("Zero-overhead progress tracking", output)
        
    @patch('sys.argv', ['cursor-eta', '--demo'])
    @patch('time.sleep')  # Speed up test
    def test_demo_mode(self, mock_sleep):
        """Test --demo flag."""
        with patch('builtins.print') as mock_print:
            main()
            
        # Check that demo was run
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("cursor-eta Demo" in call for call in print_calls))
        self.assertTrue(any("AI Code Generation" in call for call in print_calls))
        
    @patch('sys.argv', ['cursor-eta', '--demo', '--task', 'Custom Task', '--complexity', 'complex'])
    @patch('time.sleep')  # Speed up test
    def test_custom_demo_parameters(self, mock_sleep):
        """Test demo with custom parameters."""
        with patch('builtins.print') as mock_print:
            main()
            
        # Check that custom parameters were used
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("Custom Task" in call for call in print_calls))
        self.assertTrue(any("complex" in call for call in print_calls))
        
    @patch('sys.argv', ['cursor-eta'])  # No arguments
    @patch('time.sleep')  # Speed up test
    def test_no_arguments(self, mock_sleep):
        """Test running with no arguments (should run demo)."""
        with patch('builtins.print') as mock_print:
            main()
            
        # Should run demo by default
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("cursor-eta Demo" in call for call in print_calls))
        
    @patch('sys.argv', ['cursor-eta', '--invalid-flag'])
    def test_invalid_flag(self):
        """Test invalid command line flag."""
        with self.assertRaises(SystemExit) as cm:
            with patch('sys.stderr', new=StringIO()):
                main()
                
        # Should exit with error code
        self.assertNotEqual(cm.exception.code, 0)
        
    def test_main_module_execution(self):
        """Test that __main__.py can be executed as a module."""
        import cursor_eta.__main__
        
        # Should have main function
        self.assertTrue(hasattr(cursor_eta.__main__, 'main'))
        self.assertTrue(callable(cursor_eta.__main__.main))
        
    @patch('cursor_eta.__main__.demo_task')
    @patch('sys.argv', ['cursor-eta', '--demo'])
    def test_demo_task_called_correctly(self, mock_demo_task):
        """Test that demo_task is called with correct parameters."""
        mock_demo_task.return_value = "Mocked result"
        
        main()
        
        # Check that demo_task was called
        mock_demo_task.assert_called_once_with("AI Code Generation", "medium")


if __name__ == "__main__":
    unittest.main()