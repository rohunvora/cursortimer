#!/usr/bin/env python3
"""Unit tests for the cursor_eta package initialization."""

import unittest
from unittest.mock import MagicMock, patch

import cursor_eta


class TestPackageInit(unittest.TestCase):
    """Test the package initialization and exports."""

    def test_version(self):
        """Test that version is properly defined."""
        self.assertTrue(hasattr(cursor_eta, '__version__'))
        self.assertIsInstance(cursor_eta.__version__, str)
        self.assertEqual(cursor_eta.__version__, '0.1.0')

    def test_exports(self):
        """Test that all expected exports are available."""
        expected_exports = [
            'AgentETATracker',
            'AgentWrapper',
            'track_agent',
            '__version__',
        ]
        
        for export in expected_exports:
            self.assertTrue(hasattr(cursor_eta, export), f"Missing export: {export}")

    def test_agent_eta_tracker_import(self):
        """Test that AgentETATracker can be imported and instantiated."""
        tracker = cursor_eta.AgentETATracker(total_steps=10)
        self.assertEqual(tracker.total_steps, 10)

    def test_agent_wrapper_import(self):
        """Test that AgentWrapper can be imported and instantiated."""
        wrapper = cursor_eta.AgentWrapper()
        self.assertIsNotNone(wrapper)

    def test_track_agent_decorator(self):
        """Test the track_agent decorator."""
        # Test basic decoration
        @cursor_eta.track_agent(steps=3, duration=1.0)
        def sample_task():
            return "completed"
        
        with patch('time.sleep'):  # Speed up test
            with patch('sys.stdout'):  # Suppress output
                result = sample_task()
        
        self.assertEqual(result, "completed")

    def test_track_agent_decorator_with_args(self):
        """Test the track_agent decorator with function arguments."""
        @cursor_eta.track_agent(steps=2, tokens=100)
        def task_with_args(x, y, z=10):
            return x + y + z
        
        with patch('time.sleep'):
            with patch('sys.stdout'):
                result = task_with_args(1, 2, z=3)
        
        self.assertEqual(result, 6)

    def test_track_agent_decorator_no_params(self):
        """Test track_agent decorator with no parameters."""
        @cursor_eta.track_agent()
        def simple_task():
            return 42
        
        with patch('time.sleep'):
            with patch('sys.stdout'):
                result = simple_task()
        
        self.assertEqual(result, 42)

    def test_all_attribute(self):
        """Test that __all__ is properly defined if present."""
        if hasattr(cursor_eta, '__all__'):
            all_exports = cursor_eta.__all__
            self.assertIsInstance(all_exports, list)
            # Check that all items in __all__ are actually exported
            for item in all_exports:
                self.assertTrue(hasattr(cursor_eta, item), 
                               f"Item in __all__ not exported: {item}")


class TestPackageStructure(unittest.TestCase):
    """Test the package structure and dependencies."""

    def test_submodules(self):
        """Test that submodules can be imported."""
        try:
            from cursor_eta import agent_with_eta
            from cursor_eta import eta_bridge
        except ImportError as e:
            self.fail(f"Failed to import submodule: {e}")

    def test_no_circular_imports(self):
        """Test that there are no circular import issues."""
        # Force reimport to check for circular dependencies
        import importlib
        try:
            importlib.reload(cursor_eta)
        except ImportError as e:
            self.fail(f"Circular import detected: {e}")


if __name__ == "__main__":
    unittest.main()