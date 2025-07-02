#!/usr/bin/env python3
"""Unit tests for the __main__ module."""

import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from cursor_eta.__main__ import main


class TestMainModule(unittest.TestCase):
    """Test the CLI entry point functionality."""

    def test_help_command(self):
        """Test the help command."""
        with patch('sys.argv', ['cursor-eta', 'help']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with self.assertRaises(SystemExit) as cm:
                    main()
                
                self.assertEqual(cm.exception.code, 0)
                output = mock_stdout.getvalue()
                self.assertIn("cursor-eta", output)
                self.assertIn("demo", output)
                self.assertIn("check", output)

    def test_version_command(self):
        """Test the version command."""
        with patch('sys.argv', ['cursor-eta', 'version']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with self.assertRaises(SystemExit) as cm:
                    main()
                
                self.assertEqual(cm.exception.code, 0)
                output = mock_stdout.getvalue()
                self.assertIn("cursor-eta version", output)
                self.assertIn("0.1.0", output)  # Assuming version is 0.1.0

    def test_check_command(self):
        """Test the check command."""
        with patch('sys.argv', ['cursor-eta', 'check']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                    main()
                
                output = mock_stdout.getvalue()
                self.assertIn("✓", output)
                self.assertIn("cursor-eta", output)

    def test_demo_command(self):
        """Test the demo command."""
        with patch('sys.argv', ['cursor-eta', 'demo']):
            # Mock the AgentWrapper to avoid actual execution
            with patch('cursor_eta.__main__.AgentWrapper') as mock_wrapper:
                mock_instance = MagicMock()
                mock_wrapper.return_value = mock_instance
                mock_instance.execute_with_eta.return_value = "Demo completed"
                
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    main()
                
                # Verify wrapper was called
                mock_instance.execute_with_eta.assert_called_once()
                output = mock_stdout.getvalue()
                self.assertIn("Demo completed", output)

    def test_decorator_command(self):
        """Test the decorator command."""
        with patch('sys.argv', ['cursor-eta', 'decorator']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('time.sleep'):  # Speed up the test
                    main()
                
                output = mock_stdout.getvalue()
                self.assertIn("Task completed", output)

    def test_unknown_command(self):
        """Test handling of unknown commands."""
        with patch('sys.argv', ['cursor-eta', 'unknown']):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with self.assertRaises(SystemExit) as cm:
                    main()
                
                self.assertEqual(cm.exception.code, 1)
                error_output = mock_stderr.getvalue()
                self.assertIn("Unknown command", error_output)
                self.assertIn("unknown", error_output)

    def test_no_command(self):
        """Test running without any command."""
        with patch('sys.argv', ['cursor-eta']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with self.assertRaises(SystemExit) as cm:
                    main()
                
                self.assertEqual(cm.exception.code, 0)
                output = mock_stdout.getvalue()
                self.assertIn("cursor-eta", output)
                self.assertIn("Available commands", output)

    def test_demo_basic_function(self):
        """Test the demo_basic function directly."""
        from cursor_eta.__main__ import demo_basic
        
        with patch('time.sleep'):  # Speed up the test
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                demo_basic()
                
                output = mock_stdout.getvalue()
                self.assertIn("Demo completed successfully!", output)
                self.assertIn("Cursor ETA", output)

    def test_demo_decorator_function(self):
        """Test the demo_decorator function."""
        from cursor_eta.__main__ import demo_decorator
        
        with patch('time.sleep'):  # Speed up the test
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                demo_decorator()
                
                output = mock_stdout.getvalue()
                self.assertIn("Processed", output)
                self.assertIn("files", output)


class TestMainModuleImports(unittest.TestCase):
    """Test module imports and initialization."""

    def test_imports(self):
        """Test that all required modules can be imported."""
        try:
            import cursor_eta.__main__
            from cursor_eta.__main__ import main
        except ImportError as e:
            self.fail(f"Failed to import main module: {e}")

    def test_main_callable(self):
        """Test that main function is callable."""
        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()