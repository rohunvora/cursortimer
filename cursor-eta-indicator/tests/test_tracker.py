"""Unit tests for AgentETATracker class."""

import unittest
import time
import threading
from unittest.mock import patch, MagicMock
from io import StringIO

from cursor_eta import AgentETATracker


class TestAgentETATracker(unittest.TestCase):
    """Test the ETA tracking functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = AgentETATracker(total_steps=5, expected_duration=10.0)
    
    def tearDown(self):
        """Clean up after tests."""
        if self.tracker.is_running:
            self.tracker.stop()
    
    def test_initialization(self):
        """Test tracker initialization with default and custom values."""
        # Test with defaults
        default_tracker = AgentETATracker()
        self.assertEqual(default_tracker.total_steps, 10)
        self.assertEqual(default_tracker.expected_duration, 30.0)
        self.assertEqual(default_tracker.current_step, 0)
        self.assertIsNone(default_tracker.start_time)
        self.assertFalse(default_tracker.is_running)
        
        # Test with custom values
        self.assertEqual(self.tracker.total_steps, 5)
        self.assertEqual(self.tracker.expected_duration, 10.0)
        self.assertEqual(self.tracker.current_step, 0)
        
    def test_start_tracking(self):
        """Test starting the tracker."""
        self.tracker.start(tokens_expected=1000)
        
        self.assertIsNotNone(self.tracker.start_time)
        self.assertTrue(self.tracker.is_running)
        self.assertEqual(self.tracker.current_step, 1)
        self.assertEqual(self.tracker.tokens_expected, 1000)
        self.assertIsNotNone(self.tracker.update_thread)
        if self.tracker.update_thread:
            self.assertTrue(self.tracker.update_thread.is_alive())
        
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
        self.assertEqual(self.tracker.step_descriptions[4], "Next step")
        
        # Test step without description
        self.tracker.step(5)
        self.assertEqual(self.tracker.current_step, 5)
        self.assertNotIn(5, self.tracker.step_descriptions)
        
    def test_token_updates(self):
        """Test updating token usage."""
        self.tracker.start(tokens_expected=500)
        
        self.tracker.update_tokens(100)
        self.assertEqual(self.tracker.tokens_used, 100)
        
        self.tracker.update_tokens(250)
        self.assertEqual(self.tracker.tokens_used, 250)
        
    def test_eta_calculation(self):
        """Test ETA calculation logic."""
        # Before starting
        eta = self.tracker.get_eta()
        self.assertEqual(eta, 10.0)  # Should return expected_duration
        
        # Start and test immediately
        self.tracker.start()
        eta = self.tracker.get_eta()
        self.assertLessEqual(eta, 10.0)
        
        # Simulate progress
        time.sleep(0.1)
        self.tracker.step(3)  # 60% complete
        eta = self.tracker.get_eta()
        
        # ETA should be reasonable based on progress
        self.assertGreaterEqual(eta, 0)
        self.assertLess(eta, 10.0)
        
    def test_status_dictionary(self):
        """Test status dictionary generation."""
        self.tracker.start(tokens_expected=1000)
        self.tracker.step(2, "Analyzing")
        self.tracker.update_tokens(200)
        
        time.sleep(0.1)  # Let some time pass
        
        status = self.tracker.get_status()
        
        # Check all required fields
        self.assertIn("eta_seconds", status)
        self.assertIn("current_step", status)
        self.assertIn("total_steps", status)
        self.assertIn("tokens_used", status)
        self.assertIn("tokens_expected", status)
        self.assertIn("elapsed_seconds", status)
        self.assertIn("progress_percent", status)
        self.assertIn("current_description", status)
        
        # Check values
        self.assertEqual(status["current_step"], 2)
        self.assertEqual(status["total_steps"], 5)
        self.assertEqual(status["tokens_used"], 200)
        self.assertEqual(status["tokens_expected"], 1000)
        self.assertEqual(status["progress_percent"], 40)
        self.assertEqual(status["current_description"], "Analyzing")
        self.assertGreaterEqual(status["elapsed_seconds"], 0)
        
    def test_stop_tracking(self):
        """Test stopping the tracker."""
        self.tracker.start()
        self.assertTrue(self.tracker.is_running)
        
        self.tracker.stop()
        self.assertFalse(self.tracker.is_running)
        
        # Thread should stop
        time.sleep(0.6)  # Wait for thread timeout
        if self.tracker.update_thread:
            self.assertFalse(self.tracker.update_thread.is_alive())
        
    def test_format_time(self):
        """Test time formatting."""
        # Seconds
        self.assertEqual(self.tracker._format_time(45), "45s")
        self.assertEqual(self.tracker._format_time(59), "59s")
        
        # Minutes
        self.assertEqual(self.tracker._format_time(60), "1m 0s")
        self.assertEqual(self.tracker._format_time(125), "2m 5s")
        self.assertEqual(self.tracker._format_time(3599), "59m 59s")
        
        # Hours
        self.assertEqual(self.tracker._format_time(3600), "1h 0m")
        self.assertEqual(self.tracker._format_time(7265), "2h 1m")
        
    def test_progress_bar(self):
        """Test progress bar generation."""
        # 0%
        bar = self.tracker._make_progress_bar(0)
        self.assertIn("[░░░░░░░░░░░░░░░░░░░░]", bar)
        self.assertIn("0%", bar)
        
        # 50%
        bar = self.tracker._make_progress_bar(50)
        self.assertIn("██████████", bar)
        self.assertIn("50%", bar)
        
        # 100%
        bar = self.tracker._make_progress_bar(100)
        self.assertIn("[████████████████████]", bar)
        self.assertIn("100%", bar)
        
    @patch('sys.stderr')
    @patch('sys.stdout')
    def test_emit_update(self, mock_stdout, mock_stderr):
        """Test update emission."""
        self.tracker.start()
        self.tracker.step(2, "Testing")
        
        # Capture output
        stderr_buffer = StringIO()
        stdout_buffer = StringIO()
        mock_stderr.write = stderr_buffer.write
        mock_stderr.flush = MagicMock()
        
        # We need to handle print() for stdout
        with patch('builtins.print') as mock_print:
            self.tracker._emit_update()
            
            # Check that print was called with STATUS|
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertTrue(call_args.startswith("STATUS|"))
            self.assertIn('"current_step": 2', call_args)
            
        # Check stderr output
        stderr_output = stderr_buffer.getvalue()
        self.assertIn("ETA:", stderr_output)
        self.assertIn("Step 2/5", stderr_output)
        
    def test_thread_safety(self):
        """Test thread safety of operations."""
        self.tracker.start()
        
        # Perform updates from multiple threads
        def update_worker(step_num):
            time.sleep(0.01 * step_num)
            self.tracker.step(step_num, f"Step {step_num}")
            self.tracker.update_tokens(step_num * 100)
        
        threads = []
        for i in range(1, 4):
            t = threading.Thread(target=update_worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Should have processed all updates
        self.assertIn(self.tracker.current_step, [1, 2, 3])
        self.assertGreater(self.tracker.tokens_used, 0)
        
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with 0 steps
        zero_tracker = AgentETATracker(total_steps=0, expected_duration=10.0)
        zero_tracker.start()
        
        # Should not crash
        status = zero_tracker.get_status()
        self.assertEqual(status["progress_percent"], 0)
        
        zero_tracker.stop()
        
        # Test with very large numbers
        large_tracker = AgentETATracker(total_steps=1000000, expected_duration=86400.0)
        large_tracker.start()
        large_tracker.step(500000)
        
        status = large_tracker.get_status()
        self.assertEqual(status["progress_percent"], 50)
        
        large_tracker.stop()


if __name__ == "__main__":
    unittest.main()