#!/usr/bin/env python3
"""
VS Code integration examples for Cursor ETA Indicator.

This demonstrates how to integrate ETA tracking with VS Code extension.
"""

import time
import json
import sys
from cursor_eta import ETABridge, AgentWrapper


def example_1_basic_bridge():
    """Example 1: Basic bridge communication with VS Code."""
    print("=== Example 1: Basic Bridge Communication ===")
    
    with ETABridge() as bridge:
        # Send start notification
        bridge.send_update({
            "type": "start",
            "total_steps": 5,
            "description": "Starting VS Code integration demo"
        })
        
        for i in range(1, 6):
            # Send progress update
            bridge.send_update({
                "type": "progress",
                "current": i,
                "total": 5,
                "description": f"Processing step {i}",
                "eta": (5 - i) * 2.0,  # Estimated 2 seconds per step
                "progress_percent": (i / 5) * 100
            })
            
            time.sleep(2.0)  # Simulate work
        
        # Send completion notification
        bridge.send_update({
            "type": "complete",
            "description": "Demo completed successfully",
            "duration": 10.0
        })
    
    print("Bridge communication completed\n")


def example_2_wrapper_with_bridge():
    """Example 2: Combine AgentWrapper with VS Code bridge."""
    print("=== Example 2: Wrapper + Bridge Integration ===")
    
    # Custom wrapper that also sends updates to VS Code
    class VSCodeWrapper(AgentWrapper):
        def __init__(self):
            super().__init__()
            self.bridge = ETABridge()
        
        def execute_with_eta(self, func, *args, **kwargs):
            # Start the bridge
            self.bridge.start()
            
            try:
                # Send start update to VS Code
                self.bridge.send_update({
                    "type": "start",
                    "total_steps": kwargs.get('eta_total_steps', 5),
                    "description": "Starting task execution"
                })
                
                # Execute the original function
                result = super().execute_with_eta(func, *args, **kwargs)
                
                # Send completion update
                self.bridge.send_update({
                    "type": "complete",
                    "description": "Task completed successfully"
                })
                
                return result
                
            finally:
                self.bridge.stop()
        
        def update_step(self, step_number=None, description=""):
            # Call parent update
            super().update_step(step_number, description)
            
            # Also send to VS Code - simplified example
            self.bridge.send_update({
                "type": "progress",
                "description": description,
                "step_number": step_number
            })
    
    # Use the custom wrapper
    wrapper = VSCodeWrapper()
    
    def demo_task():
        """Demo task that sends updates to both console and VS Code."""
        tasks = [
            "Initializing workspace",
            "Loading project files",
            "Analyzing dependencies",
            "Running validation",
            "Generating output"
        ]
        
        for i, task in enumerate(tasks, 1):
            wrapper.update_step(i, task)
            print(f"  {task}...")
            time.sleep(1.5)
            
            # Update tokens every other step
            if i % 2 == 0:
                wrapper.update_tokens(i * 100)
        
        return "Integration demo completed"
    
    result = wrapper.execute_with_eta(
        demo_task,
        eta_total_steps=5,
        eta_expected_duration=8.0,
        eta_expected_tokens=500
    )
    
    print(f"Result: {result}\n")


def example_3_error_reporting():
    """Example 3: Error reporting to VS Code."""
    print("=== Example 3: Error Reporting ===")
    
    with ETABridge() as bridge:
        try:
            bridge.send_update({
                "type": "start",
                "total_steps": 3,
                "description": "Starting error-prone task"
            })
            
            # Step 1: Success
            bridge.send_update({
                "type": "progress",
                "current": 1,
                "total": 3,
                "description": "Step 1 completed successfully",
                "progress_percent": 33.3
            })
            time.sleep(1.0)
            
            # Step 2: Error
            bridge.send_update({
                "type": "error",
                "description": "Simulated error in step 2",
                "error_message": "Connection timeout",
                "current": 2,
                "total": 3
            })
            
            # Simulate recovery
            time.sleep(1.0)
            bridge.send_update({
                "type": "progress",
                "current": 2,
                "total": 3,
                "description": "Recovered from error, retrying...",
                "progress_percent": 66.7
            })
            
            time.sleep(1.0)
            
            # Step 3: Success
            bridge.send_update({
                "type": "complete",
                "description": "All steps completed despite errors",
                "duration": 3.0
            })
            
        except Exception as e:
            bridge.send_update({
                "type": "error",
                "description": f"Fatal error: {e}",
                "error_message": str(e)
            })
    
    print("Error reporting demo completed\n")


def example_4_system_monitoring():
    """Example 4: System resource monitoring with bridge."""
    print("=== Example 4: System Monitoring ===")
    
    try:
        import psutil
        has_psutil = True
    except ImportError:
        has_psutil = False
        print("Note: psutil not available, system monitoring disabled")
    
    with ETABridge() as bridge:
        bridge.send_update({
            "type": "start",
            "total_steps": 1,
            "description": "Starting system monitoring demo"
        })
        
        # Simulate a CPU-intensive task
        print("  Simulating intensive work (system monitoring active)...")
        
        for i in range(10):
            # Send periodic updates
            update = {
                "type": "progress",
                "current": 1,
                "total": 1,
                "description": f"Intensive work iteration {i+1}/10",
                "progress_percent": ((i + 1) / 10) * 100
            }
            
            if has_psutil:
                # Add system metrics
                update.update({
                    "cpu_percent": psutil.cpu_percent(),
                    "memory_percent": psutil.virtual_memory().percent,
                    "system_load": psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
                })
            
            bridge.send_update(update)
            
            # Simulate work
            time.sleep(0.5)
        
        bridge.send_update({
            "type": "complete",
            "description": "System monitoring demo completed",
            "duration": 5.0
        })
    
    print("System monitoring demo completed\n")


def example_5_custom_protocol():
    """Example 5: Custom protocol for advanced VS Code features."""
    print("=== Example 5: Custom Protocol ===")
    
    class AdvancedBridge(ETABridge):
        """Extended bridge with custom protocol features."""
        
        def send_file_update(self, filename, status):
            """Send file-specific update."""
            self.send_update({
                "type": "file_update",
                "filename": filename,
                "status": status,
                "timestamp": time.time()
            })
        
        def send_log_message(self, level, message):
            """Send log message to VS Code."""
            self.send_update({
                "type": "log",
                "level": level,
                "message": message,
                "timestamp": time.time()
            })
        
        def send_metrics_update(self, metrics):
            """Send performance metrics."""
            self.send_update({
                "type": "metrics",
                "metrics": metrics,
                "timestamp": time.time()
            })
    
    with AdvancedBridge() as bridge:
        bridge.send_update({
            "type": "start",
            "total_steps": 4,
            "description": "Advanced protocol demo"
        })
        
        # File processing with individual file updates
        files = ["main.py", "utils.py", "config.json", "README.md"]
        
        for i, filename in enumerate(files, 1):
            bridge.send_file_update(filename, "processing")
            bridge.send_log_message("info", f"Started processing {filename}")
            
            # Simulate file processing
            time.sleep(1.0)
            
            bridge.send_file_update(filename, "completed")
            bridge.send_log_message("success", f"Completed processing {filename}")
            
            # Send progress update
            bridge.send_update({
                "type": "progress",
                "current": i,
                "total": len(files),
                "description": f"Processed {filename}",
                "progress_percent": (i / len(files)) * 100
            })
            
            # Send performance metrics
            bridge.send_metrics_update({
                "files_processed": i,
                "processing_rate": i / ((i * 1.0) + 1),
                "memory_usage": 45.2 + (i * 2.1)  # Simulated
            })
        
        bridge.send_update({
            "type": "complete",
            "description": "Advanced protocol demo completed",
            "files_processed": len(files)
        })
    
    print("Advanced protocol demo completed\n")


def main():
    """Run all VS Code integration examples."""
    print("🔗 Cursor ETA Indicator - VS Code Integration Examples\n")
    
    examples = [
        example_1_basic_bridge,
        example_2_wrapper_with_bridge,
        example_3_error_reporting,
        example_4_system_monitoring,
        example_5_custom_protocol
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
    
    print("🎉 All VS Code integration examples completed!")
    print("\nNote: VS Code extension must be installed and active to see UI updates.")


if __name__ == "__main__":
    main()