#!/usr/bin/env python3
"""Unit tests for the ETA Bridge module."""

import json
import sys
import threading
import time
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from cursor_eta.eta_bridge import ETABridge


class TestETABridge(unittest.TestCase):
    """Test the ETA Bridge functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.bridge = ETABridge()

    def tearDown(self):
        """Clean up after tests."""
        if self.bridge.is_running:
            self.bridge.stop()

    def test_initialization(self):
        """Test bridge initialization."""
        self.assertFalse(self.bridge.is_running)
        self.assertIsNone(self.bridge._monitor_thread)
        self.assertIsNotNone(self.bridge._stop_event)

    def test_send_update_not_running(self):
        """Test sending update when bridge is not running."""
        # Should not raise error, just return silently
        self.bridge.send_update({
            "type": "progress",
            "current": 1,
            "total": 10
        })

    def test_send_update_running(self):
        """Test sending update when bridge is running."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.bridge.start()
            
            # Send a progress update
            update = {
                "type": "progress",
                "current": 5,
                "total": 10,
                "description": "Processing"
            }
            self.bridge.send_update(update)
            
            # Give thread time to process
            time.sleep(0.1)
            
            output = mock_stdout.getvalue()
            self.assertIn("ETA_UPDATE", output)
            self.assertIn(json.dumps(update), output)

    def test_start_stop(self):
        """Test starting and stopping the bridge."""
        self.assertFalse(self.bridge.is_running)
        
        self.bridge.start()
        self.assertTrue(self.bridge.is_running)
        self.assertIsNotNone(self.bridge._monitor_thread)
        self.assertTrue(self.bridge._monitor_thread.is_alive())
        
        self.bridge.stop()
        self.assertFalse(self.bridge.is_running)
        # Thread should terminate
        self.bridge._monitor_thread.join(timeout=2)
        self.assertFalse(self.bridge._monitor_thread.is_alive())

    def test_double_start(self):
        """Test starting an already running bridge."""
        self.bridge.start()
        thread1 = self.bridge._monitor_thread
        
        # Second start should be no-op
        self.bridge.start()
        thread2 = self.bridge._monitor_thread
        
        self.assertIs(thread1, thread2)
        self.bridge.stop()

    def test_double_stop(self):
        """Test stopping an already stopped bridge."""
        self.bridge.start()
        self.bridge.stop()
        
        # Second stop should be no-op
        self.bridge.stop()
        self.assertFalse(self.bridge.is_running)

    def test_monitor_loop_cpu_high(self):
        """Test monitor loop with high CPU usage."""
        with patch('psutil.cpu_percent', return_value=85.0):
            with patch('psutil.virtual_memory') as mock_mem:
                mock_mem.return_value = MagicMock(percent=60.0)
                
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    self.bridge.start()
                    time.sleep(0.15)  # Allow one monitor cycle
                    
                    output = mock_stdout.getvalue()
                    self.assertIn("ETA_UPDATE", output)
                    self.assertIn('"type": "system"', output)
                    self.assertIn('"cpu_percent": 85.0', output)
                    self.assertIn('"memory_percent": 60.0', output)

    def test_monitor_loop_memory_high(self):
        """Test monitor loop with high memory usage."""
        with patch('psutil.cpu_percent', return_value=50.0):
            with patch('psutil.virtual_memory') as mock_mem:
                mock_mem.return_value = MagicMock(percent=85.0)
                
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    self.bridge.start()
                    time.sleep(0.15)  # Allow one monitor cycle
                    
                    output = mock_stdout.getvalue()
                    self.assertIn("ETA_UPDATE", output)
                    self.assertIn('"memory_percent": 85.0', output)

    def test_context_manager(self):
        """Test using bridge as context manager."""
        with patch('sys.stdout', new_callable=StringIO):
            with ETABridge() as bridge:
                self.assertTrue(bridge.is_running)
                bridge.send_update({"type": "test"})
            
            # Should be stopped after exiting context
            self.assertFalse(bridge.is_running)

    def test_error_handling(self):
        """Test error handling in monitor loop."""
        with patch('psutil.cpu_percent', side_effect=Exception("Test error")):
            # Should not crash the monitor thread
            self.bridge.start()
            time.sleep(0.15)
            
            # Bridge should still be running despite error
            self.assertTrue(self.bridge.is_running)
            self.bridge.stop()

    def test_update_types(self):
        """Test different update types."""
        updates = [
            {"type": "start", "total_steps": 10},
            {"type": "progress", "current": 5, "total": 10},
            {"type": "complete", "duration": 5.2},
            {"type": "error", "message": "Test error"},
            {"type": "log", "level": "info", "message": "Test log"},
        ]
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.bridge.start()
            
            for update in updates:
                self.bridge.send_update(update)
            
            time.sleep(0.1)
            output = mock_stdout.getvalue()
            
            for update in updates:
                self.assertIn(json.dumps(update), output)

    def test_json_encoding(self):
        """Test JSON encoding of various data types."""
        import datetime
        
        # Custom object that's not JSON serializable
        class CustomObj:
            def __str__(self):
                return "CustomObject"
        
        update = {
            "type": "data",
            "timestamp": datetime.datetime.now(),
            "custom": CustomObj(),
            "number": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"key": "value"}
        }
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.bridge.start()
            
            # Should handle non-serializable objects gracefully
            self.bridge.send_update(update)
            time.sleep(0.1)
            
            output = mock_stdout.getvalue()
            # Should contain the update (with serializable parts)
            self.assertIn("ETA_UPDATE", output)
            self.assertIn('"type": "data"', output)


if __name__ == "__main__":
    unittest.main()