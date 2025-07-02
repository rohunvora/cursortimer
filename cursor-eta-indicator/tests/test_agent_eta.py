#!/usr/bin/env python3
"""
Unit tests for the agent ETA wrapper.
"""

import unittest
import time
import json
import threading
from io import StringIO
import sys
from unittest.mock import patch, MagicMock

from cursor_eta.agent_with_eta import AgentETATracker, AgentWrapper


class TestAgentETATracker(unittest.TestCase):
    """Test the ETA tracking functionality."""
    
    def setUp(self):
        self.tracker = AgentETATracker(total_steps=5, expected_duration=10.0)
    
    def test_initialization(self):
        """Test tracker initialization."""
        self.assertEqual(self.tracker.total_steps, 5)
        self.assertEqual(self.tracker.expected_duration, 10.0)
        self.assertEqual(self.tracker.current_step, 0)
        self.assertIsNone(self.tracker.start_time)
        
    def test_start_tracking(self):
        """Test starting the tracker."""
        self.tracker.start(tokens_expected=500)
        self.assertIsNotNone(self.tracker.start_time)
        self.assertTrue(self.tracker.is_running)
        self.assertEqual(self.tracker.tokens_expected, 500)
        self.assertEqual(self.tracker.current_step, 1)
        
        # Clean up
        self.tracker.stop()
        
    def test_step_updates(self):
        """Test updating steps."""
        self.tracker.start()
        
        # Test explicit step number
        self.tracker.step(3, "Processing data")
        self.assertEqual(self.tracker.current_step, 3)
        self.assertEqual(self.tracker.step_descriptions[3], "Processing data")
        
        # Test auto-increment
        self.tracker.step(description="Next step")
        self.assertEqual(self.tracker.current_step, 4)
        
        self.tracker.stop()
        
    def test_eta_calculation(self):
        """Test ETA calculation logic."""
        # Before start, should return expected duration
        self.assertEqual(self.tracker.get_eta(), 10.0)
        
        # Start and advance
        self.tracker.start()
        time.sleep(0.1)
        
        # At step 1 of 5, with 0.1s elapsed
        eta = self.tracker.get_eta()
        self.assertGreater(eta, 0)
        self.assertLess(eta, 10.0)
        
        # Advance to step 3
        self.tracker.step(3)
        eta2 = self.tracker.get_eta()
        self.assertLess(eta2, eta)  # ETA should decrease
        
        self.tracker.stop()
        
    def test_status_output(self):
        """Test status dictionary generation."""
        self.tracker.start(tokens_expected=1000)
        self.tracker.step(2, "Testing")
        self.tracker.update_tokens(200)
        
        status = self.tracker.get_status()
        
        self.assertEqual(status["current_step"], 2)
        self.assertEqual(status["total_steps"], 5)
        self.assertEqual(status["tokens_used"], 200)
        self.assertEqual(status["tokens_expected"], 1000)
        self.assertEqual(status["progress_percent"], 40)
        self.assertEqual(status["current_description"], "Testing")
        
        self.tracker.stop()
        
    def test_format_time(self):
        """Test time formatting."""
        tracker = self.tracker
        
        # Test seconds
        self.assertEqual(tracker._format_time(45), "45s")
        
        # Test minutes
        self.assertEqual(tracker._format_time(90), "1m 30s")
        
        # Test hours
        self.assertEqual(tracker._format_time(3661), "1h 1m")
        
    def test_progress_bar(self):
        """Test progress bar generation."""
        bar = self.tracker._make_progress_bar(0, width=10)
        self.assertEqual(bar, "[░░░░░░░░░░] 0%")
        
        bar = self.tracker._make_progress_bar(50, width=10)
        self.assertEqual(bar, "[█████░░░░░] 50%")
        
        bar = self.tracker._make_progress_bar(100, width=10)
        self.assertEqual(bar, "[██████████] 100%")


class TestAgentWrapper(unittest.TestCase):
    """Test the agent wrapper functionality."""
    
    def setUp(self):
        self.wrapper = AgentWrapper()
        
    def test_execute_with_eta(self):
        """Test executing a function with ETA tracking."""
        def mock_task():
            return "Task completed"
            
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.wrapper.execute_with_eta(
                mock_task,
                eta_total_steps=3,
                eta_expected_duration=1.0
            )
            
        self.assertEqual(result, "Task completed")
        output = mock_stdout.getvalue()
        self.assertIn("STATUS|COMPLETE", output)
        
    def test_wrapper_updates(self):
        """Test wrapper update methods."""
        def mock_task():
            self.wrapper.update_step(2, "Step 2")
            self.wrapper.update_tokens(100)
            return "Done"
            
        with patch('sys.stdout', new_callable=StringIO):
            result = self.wrapper.execute_with_eta(
                mock_task,
                eta_total_steps=5
            )
            
        self.assertEqual(result, "Done")


class TestIntegration(unittest.TestCase):
    """Integration tests for the full system."""
    
    def test_full_workflow(self):
        """Test a complete workflow with progress tracking."""
        wrapper = AgentWrapper()
        steps_executed = []
        
        def complex_task():
            for i in range(1, 4):
                wrapper.update_step(i, f"Step {i}")
                steps_executed.append(i)
                time.sleep(0.05)  # Simulate work
            return "Success"
            
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                result = wrapper.execute_with_eta(
                    complex_task,
                    eta_total_steps=3,
                    eta_expected_duration=0.2
                )
                
        self.assertEqual(result, "Success")
        self.assertEqual(steps_executed, [1, 2, 3])
        
        # Check that status updates were emitted
        stdout_content = mock_stdout.getvalue()
        self.assertIn("STATUS|", stdout_content)
        self.assertIn("STATUS|COMPLETE", stdout_content)
        
        # Check that progress bars were shown
        stderr_content = mock_stderr.getvalue()
        self.assertIn("ETA:", stderr_content)
        self.assertIn("Step", stderr_content)


if __name__ == "__main__":
    unittest.main()