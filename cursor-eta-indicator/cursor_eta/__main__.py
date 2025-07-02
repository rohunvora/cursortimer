"""
Command-line interface for cursor-eta.

Run with: python -m cursor_eta
"""

import sys
import argparse
import time
from . import AgentWrapper, __version__


def demo_task(name: str, complexity: str):
    """Demo task showing ETA tracking."""
    wrapper = AgentWrapper()
    
    complexities = {
        "simple": (3, 5.0, ["Initializing", "Processing", "Completing"]),
        "medium": (5, 15.0, ["Scanning", "Analyzing", "Building", "Testing", "Finalizing"]),
        "complex": (8, 30.0, ["Scanning", "Parsing", "Analyzing", "Planning", 
                              "Implementing", "Testing", "Optimizing", "Reviewing"])
    }
    
    steps, duration, descriptions = complexities.get(complexity, complexities["medium"])
    
    print(f"\n🚀 Starting: {name}")
    print(f"📊 Complexity: {complexity} ({steps} steps, ~{duration}s expected)")
    print("-" * 50)
    
    def run_demo():
        for i, desc in enumerate(descriptions, 1):
            wrapper.update_step(i, desc)
            # Simulate work with variable duration
            time.sleep(duration / steps * (0.8 + i * 0.1))
            if i % 2 == 0:
                wrapper.update_tokens(i * 100)
        return f"✅ Completed {name} successfully!"
    
    result = wrapper.execute_with_eta(
        run_demo,
        eta_total_steps=steps,
        eta_expected_duration=duration,
        eta_expected_tokens=steps * 100
    )
    
    return result


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="cursor-eta: Zero-overhead progress tracking for Cursor AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m cursor_eta                    # Run interactive demo
  python -m cursor_eta --demo             # Run quick demo
  python -m cursor_eta --version          # Show version
  
For integration:
  from cursor_eta import track_agent
  
  @track_agent(steps=5, duration=20.0)
  def my_agent_task():
      # Your agent code here
      pass
        """
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"cursor-eta {__version__}"
    )
    
    parser.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run a quick demo"
    )
    
    parser.add_argument(
        "--task", "-t",
        default="AI Code Generation",
        help="Task name for demo (default: 'AI Code Generation')"
    )
    
    parser.add_argument(
        "--complexity", "-c",
        choices=["simple", "medium", "complex"],
        default="medium",
        help="Demo complexity level"
    )
    
    args = parser.parse_args()
    
    if args.demo or len(sys.argv) == 1:
        # Run demo
        print("\n🎯 cursor-eta Demo")
        print("=" * 50)
        print("Watch the ETA timer update in real-time!")
        print("Note: In production, this integrates with your actual agent code.\n")
        
        result = demo_task(args.task, args.complexity)
        print(f"\n{result}")
        print("\n💡 To integrate with your code:")
        print("   pip install cursor-eta")
        print("   from cursor_eta import track_agent")
        print("\n📚 Full docs: https://github.com/cursor-eta/cursor-eta")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()