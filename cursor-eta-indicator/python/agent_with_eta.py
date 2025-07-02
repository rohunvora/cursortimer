#!/usr/bin/env python3
"""
Lightweight ETA/Progress indicator for Cursor Agent calls.
Zero token overhead - all tracking happens after prompt submission.
"""

import sys
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class AgentETATracker:
    """Tracks progress and ETA for agent operations."""
    
    def __init__(self, total_steps: int = 10, expected_duration: float = 30.0):
        self.total_steps = total_steps
        self.current_step = 0
        self.expected_duration = expected_duration
        self.start_time = None
        self.tokens_used = 0
        self.tokens_expected = 0
        self.is_running = False
        self.update_thread = None
        self.step_descriptions = {}
        
    def start(self, tokens_expected: int = 0):
        """Start tracking with optional expected token count."""
        self.start_time = time.time()
        self.tokens_expected = tokens_expected
        self.is_running = True
        self.current_step = 1
        
        # Start update thread for continuous updates
        self.update_thread = threading.Thread(target=self._update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        
    def step(self, step_num: Optional[int] = None, description: str = ""):
        """Update current step with optional description."""
        if step_num is not None:
            self.current_step = step_num
        else:
            self.current_step += 1
            
        if description:
            self.step_descriptions[self.current_step] = description
            
    def update_tokens(self, tokens: int):
        """Update token usage."""
        self.tokens_used = tokens
        
    def stop(self):
        """Stop tracking."""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=0.5)
            
    def get_eta(self) -> float:
        """Calculate ETA in seconds."""
        if not self.start_time:
            return self.expected_duration
            
        elapsed = time.time() - self.start_time
        progress = self.current_step / self.total_steps
        
        if progress > 0:
            # Estimate based on current progress
            total_expected = elapsed / progress
            remaining = total_expected - elapsed
            return max(0, remaining)
        else:
            # Use expected duration minus elapsed
            return max(0, self.expected_duration - elapsed)
            
    def get_status(self) -> Dict[str, Any]:
        """Get current status as dictionary."""
        eta_seconds = self.get_eta()
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        return {
            "eta_seconds": round(eta_seconds),
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "tokens_used": self.tokens_used,
            "tokens_expected": self.tokens_expected,
            "elapsed_seconds": round(elapsed),
            "progress_percent": round((self.current_step / self.total_steps) * 100),
            "current_description": self.step_descriptions.get(self.current_step, "")
        }
        
    def _update_loop(self):
        """Background thread to emit updates."""
        while self.is_running:
            self._emit_update()
            time.sleep(0.5)  # Update every 500ms
            
    def _emit_update(self):
        """Emit update in both human and machine readable formats."""
        status = self.get_status()
        
        # Human readable for console (rewritable line)
        eta_str = self._format_time(status["eta_seconds"])
        progress_bar = self._make_progress_bar(status["progress_percent"])
        console_line = f"\rETA: {eta_str} | Step {status['current_step']}/{status['total_steps']} {progress_bar}"
        
        # Write to stderr for console visibility
        sys.stderr.write(console_line)
        sys.stderr.flush()
        
        # Machine readable for VS Code extension (stdout)
        machine_line = f"STATUS|{json.dumps(status)}"
        print(machine_line, flush=True)
        
    def _format_time(self, seconds: float) -> str:
        """Format seconds into human readable time."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds/60)}m {int(seconds%60)}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"
            
    def _make_progress_bar(self, percent: int, width: int = 20) -> str:
        """Create a simple ASCII progress bar."""
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percent}%"


class AgentWrapper:
    """Wrapper for agent execution with ETA tracking."""
    
    def __init__(self):
        self.tracker = None
        
    def execute_with_eta(self, agent_func, *args, **kwargs):
        """Execute an agent function with ETA tracking."""
        # Extract tracking parameters
        total_steps = kwargs.pop('eta_total_steps', 10)
        expected_duration = kwargs.pop('eta_expected_duration', 30.0)
        expected_tokens = kwargs.pop('eta_expected_tokens', 0)
        
        # Initialize tracker
        self.tracker = AgentETATracker(total_steps, expected_duration)
        self.tracker.start(expected_tokens)
        
        try:
            # Execute the actual agent function
            result = agent_func(*args, **kwargs)
            return result
        finally:
            # Stop tracking
            self.tracker.stop()
            # Clear the console line
            sys.stderr.write("\r" + " " * 80 + "\r")
            sys.stderr.flush()
            # Final status
            print("STATUS|COMPLETE", flush=True)
            
    def update_step(self, step: Optional[int] = None, description: str = ""):
        """Update current step."""
        if self.tracker:
            self.tracker.step(step, description)
            
    def update_tokens(self, tokens: int):
        """Update token usage."""
        if self.tracker:
            self.tracker.update_tokens(tokens)


# Example usage and testing
if __name__ == "__main__":
    import random
    
    def mock_agent_task():
        """Simulate a long-running agent task."""
        wrapper = AgentWrapper()
        
        # Simulate steps
        for i in range(1, 11):
            wrapper.update_step(i, f"Processing step {i}")
            time.sleep(random.uniform(0.5, 2.0))
            
            # Simulate token usage
            if i % 3 == 0:
                wrapper.update_tokens(i * 100)
                
        return "Task completed!"
        
    # Create wrapper and execute
    wrapper = AgentWrapper()
    result = wrapper.execute_with_eta(
        mock_agent_task,
        eta_total_steps=10,
        eta_expected_duration=15.0,
        eta_expected_tokens=1000
    )
    
    print(f"\nResult: {result}")