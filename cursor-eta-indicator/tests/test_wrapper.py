"""Unit tests for AgentWrapper class."""

import unittest
import time
import sys
from unittest.mock import patch, MagicMock, call
from io import StringIO

from cursor_eta import AgentWrapper


class TestAgentWrapper(unittest.TestCase):
    """Test the AgentWrapper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.wrapper = AgentWrapper()
        
    def tearDown(self):
        """Clean up after tests."""
        if self.wrapper.tracker and self.wrapper.tracker.is_running:
            self.wrapper.tracker.stop()
    
    def test_initialization(self):
        """Test wrapper initialization."""
        self.assertIsNone(self.wrapper.tracker)
        
    def test_execute_with_eta_basic(self):
        """Test basic execution with ETA tracking."""
        def simple_task():
            return "Task completed"
        
        result = self.wrapper.execute_with_eta(
            simple_task,
            eta_total_steps=3,
            eta_expected_duration=1.0
        )
        
        self.assertEqual(result, "Task completed")
        self.assertIsNotNone(self.wrapper.tracker)
        if self.wrapper.tracker:
            self.assertFalse(self.wrapper.tracker.is_running)
        
    def test_execute_with_eta_with_args(self):
        """Test execution with arguments."""
        def task_with_args(x, y, name="test"):
            return f"{name}: {x + y}"
        
        result = self.wrapper.execute_with_eta(
            task_with_args,
            10, 20,
            name="sum",
            eta_total_steps=1,
            eta_expected_duration=0.5
        )
        
        self.assertEqual(result, "sum: 30")
        
    def test_execute_with_eta_with_updates(self):
        """Test execution with step and token updates."""
        def task_with_updates():
            self.wrapper.update_step(1, "Starting")
            time.sleep(0.1)
            self.wrapper.update_tokens(100)
            
            self.wrapper.update_step(2, "Processing")
            time.sleep(0.1)
            self.wrapper.update_tokens(300)
            
            self.wrapper.update_step(3, "Finishing")
            return "Done"
        
        result = self.wrapper.execute_with_eta(
            task_with_updates,
            eta_total_steps=3,
            eta_expected_duration=1.0,
            eta_expected_tokens=500
        )
        
        self.assertEqual(result, "Done")
        if self.wrapper.tracker:
            self.assertEqual(self.wrapper.tracker.current_step, 3)
            self.assertEqual(self.wrapper.tracker.tokens_used, 300)
        
    def test_execute_with_eta_exception_handling(self):
        """Test that tracker stops even if function raises exception."""
        def failing_task():
            self.wrapper.update_step(1, "Starting")
            raise ValueError("Test error")
        
        with self.assertRaises(ValueError):
            self.wrapper.execute_with_eta(
                failing_task,
                eta_total_steps=2,
                eta_expected_duration=1.0
            )
        
        # Tracker should be stopped
        if self.wrapper.tracker:
            self.assertFalse(self.wrapper.tracker.is_running)
        
    def test_update_methods_without_tracker(self):
        """Test update methods when no tracker is active."""
        # Should not raise exceptions
        self.wrapper.update_step(1, "Test")
        self.wrapper.update_tokens(100)
        
        # No tracker should be created
        self.assertIsNone(self.wrapper.tracker)
        
    @patch('sys.stderr')
    @patch('builtins.print')
    def test_output_clearing(self, mock_print, mock_stderr):
        """Test that console line is cleared after execution."""
        mock_stderr.write = MagicMock()
        mock_stderr.flush = MagicMock()
        
        def quick_task():
            return "Done"
        
        self.wrapper.execute_with_eta(
            quick_task,
            eta_total_steps=1,
            eta_expected_duration=0.1
        )
        
        # Check that clear line was written
        clear_calls = [call for call in mock_stderr.write.call_args_list 
                      if "\r" + " " * 80 + "\r" in str(call)]
        self.assertGreater(len(clear_calls), 0)
        
        # Check that STATUS|COMPLETE was printed
        complete_calls = [call for call in mock_print.call_args_list 
                         if "STATUS|COMPLETE" in str(call)]
        self.assertGreater(len(complete_calls), 0)
        
    def test_nested_wrapper_usage(self):
        """Test using wrapper within wrapper (should work independently)."""
        outer_wrapper = AgentWrapper()
        inner_wrapper = AgentWrapper()
        
        def inner_task():
            inner_wrapper.update_step(1, "Inner task")
            return "Inner done"
        
        def outer_task():
            outer_wrapper.update_step(1, "Outer task")
            result = inner_wrapper.execute_with_eta(
                inner_task,
                eta_total_steps=1,
                eta_expected_duration=0.1
            )
            return f"Outer done, {result}"
        
        result = outer_wrapper.execute_with_eta(
            outer_task,
            eta_total_steps=1,
            eta_expected_duration=0.5
        )
        
        self.assertEqual(result, "Outer done, Inner done")
        
    def test_default_parameters(self):
        """Test execution with default tracking parameters."""
        def default_task():
            # Should use defaults: 10 steps, 30s duration, 0 tokens
            return "Default done"
        
        # Don't pass any eta_ parameters
        result = self.wrapper.execute_with_eta(default_task)
        
        self.assertEqual(result, "Default done")
        if self.wrapper.tracker:
            self.assertEqual(self.wrapper.tracker.total_steps, 10)
            self.assertEqual(self.wrapper.tracker.expected_duration, 30.0)
            self.assertEqual(self.wrapper.tracker.tokens_expected, 0)
        
    def test_concurrent_wrappers(self):
        """Test multiple wrappers running concurrently."""
        import threading
        
        results = {}
        
        def run_wrapper(wrapper_id):
            wrapper = AgentWrapper()
            
            def task():
                wrapper.update_step(1, f"Task {wrapper_id}")
                time.sleep(0.1)
                return f"Result {wrapper_id}"
            
            results[wrapper_id] = wrapper.execute_with_eta(
                task,
                eta_total_steps=1,
                eta_expected_duration=0.5
            )
        
        threads = []
        for i in range(3):
            t = threading.Thread(target=run_wrapper, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # All tasks should complete successfully
        self.assertEqual(len(results), 3)
        for i in range(3):
            self.assertEqual(results[i], f"Result {i}")


if __name__ == "__main__":
    unittest.main()