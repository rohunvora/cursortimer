#!/usr/bin/env python3
"""
Bridge module for communication between Python wrapper and VS Code extension.
This handles ETA updates and system monitoring.
"""

import json
import random
import sys
import threading
import time
from typing import Any, Dict, Optional

try:
    import psutil
except ImportError:
    psutil = None

from .agent_with_eta import AgentWrapper


class ETABridge:
    """Bridge for communication between Python and VS Code extension."""
    
    def __init__(self):
        """Initialize the ETA bridge."""
        self.is_running = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._update_queue = []
        
    def start(self):
        """Start the bridge monitoring."""
        if self.is_running:
            return
            
        self.is_running = True
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        
    def stop(self):
        """Stop the bridge monitoring."""
        if not self.is_running:
            return
            
        self.is_running = False
        self._stop_event.set()
        
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)
            
    def send_update(self, update: Dict[str, Any]):
        """Send an update to the VS Code extension."""
        if not self.is_running:
            return
            
        try:
            # Send update via stdout (captured by VS Code)
            print(f"ETA_UPDATE:{json.dumps(update, default=str)}", flush=True)
        except Exception:
            pass  # Silently ignore JSON encoding errors
            
    def _monitor_loop(self):
        """Monitor system resources and send updates."""
        while not self._stop_event.is_set():
            try:
                if psutil:
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    memory_percent = psutil.virtual_memory().percent
                    
                    # Send system update if resources are high
                    if cpu_percent > 80 or memory_percent > 80:
                        self.send_update({
                            "type": "system",
                            "cpu_percent": cpu_percent,
                            "memory_percent": memory_percent,
                            "timestamp": time.time()
                        })
                        
            except Exception:
                pass  # Ignore monitoring errors
                
            # Wait before next check
            self._stop_event.wait(0.1)
            
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


def example_cursor_agent_task(task_name: str, complexity: str = "medium"):
    """
    Example of how a Cursor agent task would be wrapped with ETA tracking.
    This simulates various agent operations.
    """
    # Get the global wrapper instance
    wrapper = agent_wrapper
    
    # Define task steps based on complexity
    steps = {
        "simple": [
            ("Analyzing request", 1.0),
            ("Generating code", 2.0),
            ("Validating output", 0.5)
        ],
        "medium": [
            ("Parsing codebase", 2.0),
            ("Analyzing dependencies", 1.5),
            ("Planning changes", 1.0),
            ("Generating code", 3.0),
            ("Running tests", 2.0),
            ("Finalizing", 0.5)
        ],
        "complex": [
            ("Scanning repository", 3.0),
            ("Building dependency graph", 2.0),
            ("Analyzing patterns", 2.5),
            ("Planning refactor", 2.0),
            ("Generating changes", 4.0),
            ("Validating changes", 2.0),
            ("Running test suite", 3.0),
            ("Optimizing output", 1.5),
            ("Final review", 1.0)
        ]
    }
    
    task_steps = steps.get(complexity, steps["medium"])
    
    # Simulate task execution
    for i, (description, duration) in enumerate(task_steps, 1):
        wrapper.update_step(i, description)
        
        # Simulate work with variable duration
        actual_duration = duration * random.uniform(0.7, 1.3)
        time.sleep(actual_duration)
        
        # Update token usage periodically
        if i % 2 == 0:
            tokens = i * random.randint(50, 150)
            wrapper.update_tokens(tokens)
    
    return f"Completed {task_name} with {len(task_steps)} steps"


# Global wrapper instance
agent_wrapper = AgentWrapper()


def run_agent_task(task_name: str, complexity: str = "medium"):
    """
    Entry point for running an agent task with ETA tracking.
    """
    # Map complexity to expected duration and steps
    complexity_map = {
        "simple": (5.0, 3),
        "medium": (15.0, 6),
        "complex": (30.0, 9)
    }
    
    expected_duration, total_steps = complexity_map.get(complexity, (15.0, 6))
    expected_tokens = total_steps * 100
    
    # Execute with ETA tracking
    result = agent_wrapper.execute_with_eta(
        example_cursor_agent_task,
        task_name,
        complexity,
        eta_total_steps=total_steps,
        eta_expected_duration=expected_duration,
        eta_expected_tokens=expected_tokens
    )
    
    return result


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Cursor agent task with ETA tracking")
    parser.add_argument("task", nargs="?", default="Code refactoring", help="Task description")
    parser.add_argument("--complexity", choices=["simple", "medium", "complex"], 
                       default="medium", help="Task complexity")
    
    args = parser.parse_args()
    
    print(f"\nStarting task: {args.task} (complexity: {args.complexity})\n")
    result = run_agent_task(args.task, args.complexity)
    print(f"\n{result}\n")