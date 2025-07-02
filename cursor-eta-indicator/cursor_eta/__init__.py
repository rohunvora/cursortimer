"""
Cursor ETA Indicator - ETA indicators for cursor AI coding tasks.

This package provides ETA (Estimated Time to Arrival) indicators for AI-powered
coding tasks in Cursor IDE, helping developers track progress and manage expectations.
"""

__version__ = "0.1.0"
__author__ = "Your Name"  # TODO: Update with actual author
__email__ = "your.email@example.com"  # TODO: Update with actual email

from .agent_with_eta import AgentETATracker, AgentWrapper
from .eta_bridge import ETABridge

__all__ = [
    # Main classes
    "AgentETATracker",
    "AgentWrapper",
    "ETABridge",
    # Convenience functions
    "track_agent",
    # Version info
    "__version__",
    "__author__",
    "__email__",
]

# Package metadata
def get_version() -> str:
    """Get the current version of cursor-eta."""
    return __version__

# Convenience function for quick usage
def track_agent(func=None, *, steps=10, duration=30.0, tokens=0):
    """
    Decorator/function to track agent execution with ETA.
    
    Can be used as a decorator:
        @track_agent(steps=5, duration=10.0)
        def my_agent_function():
            ...
            
    Or as a function wrapper:
        result = track_agent(my_function, steps=5)(arg1, arg2)
    """
    def decorator(f):
        def wrapped(*args, **kwargs):
            wrapper = AgentWrapper()
            return wrapper.execute_with_eta(
                f, *args, 
                eta_total_steps=steps,
                eta_expected_duration=duration,
                eta_expected_tokens=tokens,
                **kwargs
            )
        return wrapped
        
    if func is None:
        return decorator
    else:
        return decorator(func)