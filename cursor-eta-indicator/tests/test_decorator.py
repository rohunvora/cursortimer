"""Unit tests for track_agent decorator."""

import unittest
import time
from unittest.mock import patch

from cursor_eta import track_agent


class TestTrackAgentDecorator(unittest.TestCase):
    """Test the @track_agent decorator functionality."""
    
    def test_decorator_basic(self):
        """Test basic decorator usage."""
        @track_agent(steps=3, duration=1.0)
        def simple_task():
            time.sleep(0.1)
            return "Task done"
        
        result = simple_task()
        self.assertEqual(result, "Task done")
        
    def test_decorator_with_args(self):
        """Test decorator with function arguments."""
        @track_agent(steps=2, duration=0.5, tokens=100)
        def add_numbers(a, b, multiplier=1):
            time.sleep(0.1)
            return (a + b) * multiplier
        
        result = add_numbers(5, 3, multiplier=2)
        self.assertEqual(result, 16)
        
        # Test with positional args only
        result = add_numbers(10, 20)
        self.assertEqual(result, 30)
        
    def test_decorator_preserves_function_metadata(self):
        """Test that decorator preserves function name and docstring."""
        @track_agent(steps=1)
        def documented_function():
            """This is a test function."""
            return True
        
        # Function metadata should be preserved
        self.assertEqual(documented_function.__name__, "documented_function")
        self.assertEqual(documented_function.__doc__, "This is a test function.")
        
    def test_decorator_exception_handling(self):
        """Test decorator handles exceptions properly."""
        @track_agent(steps=2, duration=1.0)
        def failing_function():
            time.sleep(0.1)
            raise RuntimeError("Test error")
        
        with self.assertRaises(RuntimeError) as cm:
            failing_function()
        
        self.assertEqual(str(cm.exception), "Test error")
        
    def test_decorator_with_class_methods(self):
        """Test decorator works with class methods."""
        class TestClass:
            def __init__(self):
                self.value = 10
            
            @track_agent(steps=2, duration=0.5)
            def process(self, increment):
                time.sleep(0.1)
                self.value += increment
                return self.value
        
        obj = TestClass()
        result = obj.process(5)
        self.assertEqual(result, 15)
        self.assertEqual(obj.value, 15)
        
    @patch('builtins.print')
    def test_decorator_output(self, mock_print):
        """Test that decorator produces expected output."""
        @track_agent(steps=1, duration=0.1)
        def quick_task():
            return "Quick"
        
        result = quick_task()
        self.assertEqual(result, "Quick")
        
        # Should have printed STATUS messages
        status_calls = [call for call in mock_print.call_args_list 
                       if "STATUS|" in str(call)]
        self.assertGreater(len(status_calls), 0)
        
        # Should have printed STATUS|COMPLETE
        complete_calls = [call for call in mock_print.call_args_list 
                         if "STATUS|COMPLETE" in str(call)]
        self.assertEqual(len(complete_calls), 1)
        
    def test_decorator_multiple_calls(self):
        """Test decorator can be called multiple times."""
        call_count = 0
        
        @track_agent(steps=1, duration=0.1)
        def counting_function():
            nonlocal call_count
            call_count += 1
            return call_count
        
        # Call multiple times
        result1 = counting_function()
        result2 = counting_function()
        result3 = counting_function()
        
        self.assertEqual(result1, 1)
        self.assertEqual(result2, 2)
        self.assertEqual(result3, 3)
        self.assertEqual(call_count, 3)
        
    def test_decorator_with_generator(self):
        """Test decorator with generator functions."""
        @track_agent(steps=3, duration=0.3)
        def number_generator(n):
            for i in range(n):
                time.sleep(0.05)
                yield i
        
        # Collect results
        results = list(number_generator(5))
        self.assertEqual(results, [0, 1, 2, 3, 4])
        
    def test_decorator_with_async_function(self):
        """Test decorator behavior with async functions (should still work)."""
        import asyncio
        
        @track_agent(steps=2, duration=0.2)
        async def async_task(value):
            await asyncio.sleep(0.1)
            return value * 2
        
        # Run async function
        result = asyncio.run(async_task(21))
        self.assertEqual(result, 42)
        
    def test_decorator_default_values(self):
        """Test decorator with default parameter values."""
        @track_agent()  # Use all defaults
        def default_task():
            return "Default"
        
        result = default_task()
        self.assertEqual(result, "Default")
        
    def test_nested_decorators(self):
        """Test nested usage of track_agent decorators."""
        @track_agent(steps=2, duration=0.2)
        def outer_task():
            @track_agent(steps=1, duration=0.1)
            def inner_task():
                return "Inner"
            
            inner_result = inner_task()
            return f"Outer: {inner_result}"
        
        result = outer_task()
        self.assertEqual(result, "Outer: Inner")


if __name__ == "__main__":
    unittest.main()