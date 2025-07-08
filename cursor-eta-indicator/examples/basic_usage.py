#!/usr/bin/env python3
"""
Basic usage example for cursor-eta package.

This demonstrates how to integrate ETA tracking with your Cursor AI agent code.
"""

from cursor_eta import track_agent, AgentWrapper
import time


# Example 1: Using the decorator
@track_agent(steps=5, duration=10.0)
def refactor_authentication_system():
    """Example agent task with automatic ETA tracking."""
    # In real usage, this would be your actual agent code
    print("Starting authentication refactor...")
    time.sleep(2)
    print("Analyzing current implementation...")
    time.sleep(2)
    print("Generating improvements...")
    time.sleep(2)
    print("Applying changes...")
    time.sleep(2)
    print("Running tests...")
    time.sleep(2)
    return "Authentication system refactored successfully!"


# Example 2: Using the wrapper directly for more control
def analyze_codebase_with_manual_tracking():
    """Example showing manual step updates."""
    wrapper = AgentWrapper()
    
    def analyze():
        # Update progress at each major step
        wrapper.update_step(1, "Scanning project structure")
        time.sleep(1.5)
        
        wrapper.update_step(2, "Analyzing dependencies")
        wrapper.update_tokens(150)  # Track token usage
        time.sleep(2.0)
        
        wrapper.update_step(3, "Identifying code patterns")
        wrapper.update_tokens(320)
        time.sleep(1.8)
        
        wrapper.update_step(4, "Generating insights")
        wrapper.update_tokens(580)
        time.sleep(2.2)
        
        wrapper.update_step(5, "Creating report")
        wrapper.update_tokens(750)
        time.sleep(1.5)
        
        return {
            "total_files": 42,
            "code_quality": "B+",
            "suggestions": 15,
            "tokens_used": 750
        }
    
    # Execute with ETA tracking
    result = wrapper.execute_with_eta(
        analyze,
        eta_total_steps=5,
        eta_expected_duration=9.0,
        eta_expected_tokens=800
    )
    
    return result


# Example 3: Using as context manager
def process_with_context_manager():
    """Example using track_agent as a context manager."""
    from cursor_eta import AgentETATracker
    
    tracker = AgentETATracker(total_steps=3, expected_duration=6.0)
    tracker.start()
    
    try:
        # Step 1
        tracker.step(1, "Initializing")
        time.sleep(2)
        
        # Step 2
        tracker.step(2, "Processing")
        tracker.update_tokens(200)
        time.sleep(2)
        
        # Step 3
        tracker.step(3, "Finalizing")
        tracker.update_tokens(400)
        time.sleep(2)
        
        return "Process completed!"
    finally:
        tracker.stop()


if __name__ == "__main__":
    print("=== Cursor ETA Examples ===\n")
    
    # Run example 1
    print("Example 1: Using @track_agent decorator")
    print("-" * 40)
    result1 = refactor_authentication_system()
    print(f"Result: {result1}\n")
    
    # Run example 2
    print("\nExample 2: Manual tracking with AgentWrapper")
    print("-" * 40)
    result2 = analyze_codebase_with_manual_tracking()
    print(f"Result: {result2}\n")
    
    # Run example 3
    print("\nExample 3: Using context manager")
    print("-" * 40)
    result3 = process_with_context_manager()
    print(f"Result: {result3}\n")
    
    print("\n✅ All examples completed!")
    print("\n💡 In production, the ETA output integrates with Cursor's UI")
    print("   and the VS Code status bar extension for real-time updates.")