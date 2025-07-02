#!/usr/bin/env python3
"""
Example integration with Cursor's agent system.
Shows how to wrap actual agent calls with ETA tracking.
"""

from agent_with_eta import AgentWrapper
import time

# Initialize the wrapper
wrapper = AgentWrapper()


def cursor_agent_refactor_auth():
    """
    Example: Simulated Cursor agent task for refactoring authentication.
    In real usage, this would be your actual agent function.
    """
    # Step 1: Analyze current authentication system
    wrapper.update_step(1, "Analyzing current auth implementation")
    # ... agent analyzes code ...
    time.sleep(2)  # Simulated work
    
    # Step 2: Identify improvement opportunities
    wrapper.update_step(2, "Identifying security improvements")
    wrapper.update_tokens(150)  # Update token usage
    # ... agent identifies issues ...
    time.sleep(1.5)
    
    # Step 3: Generate refactored code
    wrapper.update_step(3, "Generating improved auth code")
    wrapper.update_tokens(450)
    # ... agent generates new code ...
    time.sleep(3)
    
    # Step 4: Update tests
    wrapper.update_step(4, "Updating test suite")
    wrapper.update_tokens(650)
    # ... agent updates tests ...
    time.sleep(2)
    
    # Step 5: Final validation
    wrapper.update_step(5, "Validating changes")
    wrapper.update_tokens(800)
    # ... agent validates ...
    time.sleep(1)
    
    return {
        "status": "success",
        "files_changed": 12,
        "tests_updated": 8,
        "security_score": "A+"
    }


def cursor_agent_create_api():
    """
    Example: Simulated Cursor agent task for creating a new API.
    """
    steps = [
        ("Designing API structure", 2.0, 100),
        ("Creating endpoint handlers", 3.0, 300),
        ("Implementing data models", 2.5, 500),
        ("Adding validation", 1.5, 650),
        ("Generating documentation", 2.0, 850),
        ("Creating tests", 2.5, 1100)
    ]
    
    for i, (description, duration, tokens) in enumerate(steps, 1):
        wrapper.update_step(i, description)
        wrapper.update_tokens(tokens)
        time.sleep(duration)
    
    return {
        "status": "success",
        "endpoints_created": 8,
        "models_created": 5,
        "tests_created": 24
    }


# Example 1: Refactor authentication with ETA tracking
print("Example 1: Refactoring Authentication System")
print("-" * 50)

result = wrapper.execute_with_eta(
    cursor_agent_refactor_auth,
    eta_total_steps=5,
    eta_expected_duration=10.0,
    eta_expected_tokens=1000
)

print(f"\nRefactoring Result: {result}")
print()

# Example 2: Create API with different parameters
print("\nExample 2: Creating REST API")
print("-" * 50)

result = wrapper.execute_with_eta(
    cursor_agent_create_api,
    eta_total_steps=6,
    eta_expected_duration=15.0,
    eta_expected_tokens=1200
)

print(f"\nAPI Creation Result: {result}")


# Example 3: Using as a decorator (advanced usage)
class CursorAgentWithETA:
    """Decorator pattern for adding ETA to any agent function."""
    
    def __init__(self, steps=10, duration=30.0, tokens=1000):
        self.steps = steps
        self.duration = duration
        self.tokens = tokens
        self.wrapper = AgentWrapper()
    
    def __call__(self, func):
        def wrapped(*args, **kwargs):
            return self.wrapper.execute_with_eta(
                func, *args, **kwargs,
                eta_total_steps=self.steps,
                eta_expected_duration=self.duration,
                eta_expected_tokens=self.tokens
            )
        return wrapped


# Usage with decorator
@CursorAgentWithETA(steps=3, duration=5.0, tokens=500)
def quick_format_code():
    """Quick code formatting task."""
    wrapper = AgentWrapper()  # Get the global instance
    
    wrapper.update_step(1, "Parsing code")
    time.sleep(1.5)
    
    wrapper.update_step(2, "Applying format rules")
    wrapper.update_tokens(200)
    time.sleep(2.0)
    
    wrapper.update_step(3, "Final cleanup")
    wrapper.update_tokens(400)
    time.sleep(1.0)
    
    return {"formatted_lines": 1250, "issues_fixed": 23}


print("\n\nExample 3: Quick Format with Decorator")
print("-" * 50)
result = quick_format_code()
print(f"\nFormatting Result: {result}")