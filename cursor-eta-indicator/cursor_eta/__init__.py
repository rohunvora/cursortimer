"""
cursor-eta: Lightweight ETA/progress indicator for Cursor AI agent calls.

Zero token overhead progress tracking for long-running LLM operations.
"""

__version__ = "0.1.0"
__author__ = "Cursor ETA Contributors"
__license__ = "MIT"

from .agent_with_eta import AgentETATracker, AgentWrapper

__all__ = [
    "AgentETATracker",
    "AgentWrapper",
    "__version__",
]

# Convenience function for quick usage
def track_agent(func=None, *, steps=10, duration=30.0, tokens=0):
    """
    Decorator or context manager for tracking agent progress.
    
    Usage:
        @track_agent(steps=5, duration=20.0)
        def my_agent_task():
            ...
            
        # Or
        
        with track_agent(steps=5) as tracker:
            tracker.update_step(1, "Processing...")
    """
    import functools
    
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            wrapper = AgentWrapper()
            return wrapper.execute_with_eta(
                f, *args, **kwargs,
                eta_total_steps=steps,
                eta_expected_duration=duration,
                eta_expected_tokens=tokens
            )
        return decorated
    
    if func is None:
        # Called with arguments: @track_agent(steps=5)
        return decorator
    else:
        # Called without arguments: @track_agent
        return decorator(func)