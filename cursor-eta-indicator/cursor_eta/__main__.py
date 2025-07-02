#!/usr/bin/env python3
"""
Cursor ETA command-line interface.

Run a demo or check installation status.
"""

import sys
import time
import random
from typing import Optional

from .agent_with_eta import AgentWrapper
from . import __version__


def demo_basic():
    """Run a basic ETA tracking demo."""
    print("Running Cursor ETA basic demo...")
    print("This simulates a 10-step process with random delays.\n")
    
    wrapper = AgentWrapper()
    
    def demo_task():
        """Simulate a multi-step task."""
        steps = [
            "Initializing environment",
            "Loading dependencies",
            "Analyzing codebase",
            "Generating plan",
            "Implementing changes",
            "Running tests",
            "Formatting code",
            "Creating documentation",
            "Finalizing output",
            "Cleanup"
        ]
        
        for i, step_desc in enumerate(steps, 1):
            wrapper.update_step(i, step_desc)
            # Simulate work with random delay
            delay = random.uniform(0.5, 2.0)
            time.sleep(delay)
            
            # Simulate token usage every few steps
            if i % 3 == 0:
                tokens = random.randint(100, 500) * i
                wrapper.update_tokens(tokens)
                
        return "Demo completed successfully!"
    
    # Execute with ETA tracking
    result = wrapper.execute_with_eta(
        demo_task,
        eta_total_steps=10,
        eta_expected_duration=15.0,
        eta_expected_tokens=3000
    )
    
    print(f"\n{result}")
    print(f"\nCursor ETA v{__version__} - Demo finished!")


def demo_decorator():
    """Demo using the decorator syntax."""
    print("Running Cursor ETA decorator demo...")
    print("This shows how to use the @track_agent decorator.\n")
    
    from . import track_agent
    
    @track_agent(steps=5, duration=5.0, tokens=1000)
    def process_files():
        """Simulate file processing with decorator."""
        files = ["main.py", "utils.py", "config.json", "data.csv", "report.md"]
        
        # Note: When using decorator, we can't directly access the wrapper
        # This is a limitation of the decorator approach
        for i, filename in enumerate(files, 1):
            print(f"\n[Step {i}] Processing {filename}...")
            time.sleep(random.uniform(0.5, 1.5))
            
        return f"Processed {len(files)} files"
    
    result = process_files()
    print(f"\n{result}")
    print(f"\nCursor ETA v{__version__} - Decorator demo finished!")


def check_installation():
    """Check and display installation status."""
    print(f"Cursor ETA v{__version__}")
    print("-" * 40)
    
    # Check imports
    try:
        from . import AgentETATracker, AgentWrapper
        print("✓ Core modules imported successfully")
        
        # Check if eta_bridge module is importable
        try:
            from . import eta_bridge
            print("✓ eta_bridge module found")
        except ImportError:
            pass
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Check dependencies
    deps_status = []
    try:
        import psutil
        deps_status.append(f"✓ psutil {psutil.__version__}")
    except ImportError:
        deps_status.append("✗ psutil (required)")
    
    try:
        import typing_extensions
        deps_status.append("✓ typing_extensions (installed)")
    except ImportError:
        import sys
        if sys.version_info >= (3, 9):
            deps_status.append("✓ typing_extensions (not needed for Python 3.9+)")
        else:
            deps_status.append("✗ typing_extensions (required for Python < 3.9)")
    
    print("\nDependencies:")
    for status in deps_status:
        print(f"  {status}")
    
    print("\nInstallation successful! 🎉")
    print("\nUsage:")
    print("  cursor-eta          # Run demo")
    print("  cursor-eta check    # Check installation")
    print("  cursor-eta demo     # Run basic demo")
    print("  cursor-eta decorator # Run decorator demo")
    
    return True


def main(args: Optional[list] = None):
    """Main entry point for cursor-eta command."""
    if args is None:
        args = sys.argv[1:]
    
    if not args:
        # Show help when no command is given
        print(f"Cursor ETA v{__version__}")
        print("\nAvailable commands:")
        print("  demo        Run basic demo")
        print("  decorator   Run decorator demo")
        print("  check       Check installation status")
        print("  help        Show help message")
        print("  version     Show version information")
        print("\nRun 'cursor-eta help' for more information.")
        sys.exit(0)
    elif args[0] in ["check", "--check", "-c"]:
        check_installation()
    elif args[0] in ["demo", "--demo", "-d"]:
        demo_basic()
    elif args[0] in ["decorator", "--decorator"]:
        demo_decorator()
    elif args[0] in ["help", "--help", "-h"]:
        print(f"Cursor ETA v{__version__} - Command Line Interface")
        print("\nUsage: cursor-eta [command]")
        print("\nCommands:")
        print("  demo        Run basic demo (default)")
        print("  decorator   Run decorator demo")
        print("  check       Check installation status")
        print("  help        Show this help message")
        print("  version     Show version information")
        sys.exit(0)
    elif args[0] in ["version", "--version", "-v"]:
        print(f"cursor-eta version {__version__}")
        sys.exit(0)
    else:
        print(f"Unknown command: {args[0]}")
        print("Run 'cursor-eta help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()