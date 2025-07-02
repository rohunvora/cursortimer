#!/usr/bin/env python3
"""
Basic usage examples for Cursor ETA Indicator.

This demonstrates the most common ways to use the ETA tracking functionality.
"""

import time
import random
from cursor_eta import AgentWrapper, AgentETATracker, track_agent


def example_1_wrapper_basic():
    """Example 1: Basic wrapper usage with manual step updates."""
    print("=== Example 1: Basic Wrapper Usage ===")
    
    wrapper = AgentWrapper()
    
    def coding_task():
        """Simulate a coding task with multiple steps."""
        steps = [
            "Analyzing requirements",
            "Designing solution",
            "Writing code",
            "Testing",
            "Documenting"
        ]
        
        for i, step_name in enumerate(steps, 1):
            wrapper.update_step(i, step_name)
            print(f"  Working on: {step_name}")
            
            # Simulate variable work time
            time.sleep(random.uniform(0.5, 2.0))
            
            # Update token usage occasionally
            if i % 2 == 0:
                tokens = random.randint(50, 200) * i
                wrapper.update_tokens(tokens)
        
        return f"Completed all {len(steps)} steps"
    
    # Execute with ETA tracking
    result = wrapper.execute_with_eta(
        coding_task,
        eta_total_steps=5,
        eta_expected_duration=8.0,
        eta_expected_tokens=800
    )
    
    print(f"Result: {result}\n")


def example_2_decorator():
    """Example 2: Using the @track_agent decorator."""
    print("=== Example 2: Decorator Usage ===")
    
    @track_agent(steps=3, duration=5.0, tokens=500)
    def file_processor():
        """Process files with automatic ETA tracking."""
        files = ["main.py", "utils.py", "config.json"]
        
        for i, filename in enumerate(files, 1):
            print(f"  Processing: {filename}")
            # Simulate file processing
            time.sleep(random.uniform(1.0, 2.0))
            
        return f"Processed {len(files)} files successfully"
    
    result = file_processor()
    print(f"Result: {result}\n")


def example_3_manual_tracker():
    """Example 3: Manual tracker usage for fine-grained control."""
    print("=== Example 3: Manual Tracker Usage ===")
    
    tracker = AgentETATracker(total_steps=4, expected_duration=10.0)
    
    try:
        tracker.start(tokens_expected=600)
        
        # Step 1: Setup
        tracker.step(1, "Setting up environment")
        print("  Setting up environment...")
        time.sleep(1.5)
        
        # Step 2: Data processing
        tracker.step(2, "Processing data")
        print("  Processing data...")
        time.sleep(2.0)
        tracker.update_tokens(200)
        
        # Step 3: Analysis
        tracker.step(3, "Running analysis")
        print("  Running analysis...")
        time.sleep(1.8)
        tracker.update_tokens(450)
        
        # Step 4: Finalization
        tracker.step(4, "Finalizing results")
        print("  Finalizing results...")
        time.sleep(1.2)
        tracker.update_tokens(600)
        
        # Get final status
        status = tracker.get_status()
        print(f"  Final status: {status['progress_percent']:.1f}% complete")
        print(f"  Total time: {status['elapsed_time']:.1f}s")
        print(f"  Tokens used: {status['tokens_used']}")
        
    finally:
        tracker.stop()
    
    print("Manual tracking completed\n")


def example_4_error_handling():
    """Example 4: Error handling in ETA-tracked functions."""
    print("=== Example 4: Error Handling ===")
    
    wrapper = AgentWrapper()
    
    def risky_task():
        """A task that might fail partway through."""
        try:
            wrapper.update_step(1, "Starting risky operation")
            print("  Starting risky operation...")
            time.sleep(1.0)
            
            wrapper.update_step(2, "Performing calculations")
            print("  Performing calculations...")
            time.sleep(1.0)
            
            # Simulate a potential failure
            if random.random() < 0.3:  # 30% chance of failure
                raise ValueError("Calculation failed!")
            
            wrapper.update_step(3, "Saving results")
            print("  Saving results...")
            time.sleep(0.5)
            
            return "Task completed successfully"
            
        except Exception as e:
            wrapper.update_step(description=f"Error occurred: {e}")
            print(f"  Error: {e}")
            # Re-raise to let the wrapper handle it
            raise
    
    try:
        result = wrapper.execute_with_eta(
            risky_task,
            eta_total_steps=3,
            eta_expected_duration=3.0
        )
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Task failed with error: {e}")
    
    print()


def example_5_real_world_scenario():
    """Example 5: Real-world scenario - Code refactoring task."""
    print("=== Example 5: Real-world Code Refactoring ===")
    
    wrapper = AgentWrapper()
    
    def refactor_codebase():
        """Simulate a realistic code refactoring task."""
        
        # Step 1: Analyze existing code
        wrapper.update_step(1, "Analyzing existing codebase")
        print("  📊 Analyzing existing codebase...")
        time.sleep(2.0)  # Realistic analysis time
        wrapper.update_tokens(150)
        
        # Step 2: Identify patterns
        wrapper.update_step(2, "Identifying refactoring opportunities")
        print("  🔍 Identifying refactoring opportunities...")
        time.sleep(1.8)
        wrapper.update_tokens(320)
        
        # Step 3: Plan changes
        wrapper.update_step(3, "Planning refactoring strategy")
        print("  📋 Planning refactoring strategy...")
        time.sleep(1.5)
        wrapper.update_tokens(480)
        
        # Step 4: Implement changes
        wrapper.update_step(4, "Implementing refactored code")
        print("  ⚡ Implementing refactored code...")
        time.sleep(3.0)  # Most time-consuming step
        wrapper.update_tokens(850)
        
        # Step 5: Test changes
        wrapper.update_step(5, "Testing refactored code")
        print("  🧪 Testing refactored code...")
        time.sleep(2.2)
        wrapper.update_tokens(1050)
        
        # Step 6: Update documentation
        wrapper.update_step(6, "Updating documentation")
        print("  📝 Updating documentation...")
        time.sleep(1.0)
        wrapper.update_tokens(1200)
        
        return "Refactoring completed successfully! ✅"
    
    result = wrapper.execute_with_eta(
        refactor_codebase,
        eta_total_steps=6,
        eta_expected_duration=12.0,  # Expected 12 seconds
        eta_expected_tokens=1200
    )
    
    print(f"Result: {result}\n")


def main():
    """Run all examples."""
    print("🚀 Cursor ETA Indicator - Usage Examples\n")
    
    examples = [
        example_1_wrapper_basic,
        example_2_decorator,
        example_3_manual_tracker,
        example_4_error_handling,
        example_5_real_world_scenario
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except KeyboardInterrupt:
            print("❌ Example interrupted by user")
            break
        except Exception as e:
            print(f"❌ Example {i} failed: {e}\n")
        
        if i < len(examples):
            print("─" * 50)
    
    print("🎉 All examples completed!")


if __name__ == "__main__":
    main()