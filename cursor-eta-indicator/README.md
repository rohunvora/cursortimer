# Cursor ETA Indicator

[![CI](https://github.com/cursor-eta/cursor-eta/actions/workflows/ci.yml/badge.svg)](https://github.com/cursor-eta/cursor-eta/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/cursor-eta.svg)](https://badge.fury.io/py/cursor-eta)
[![Python Support](https://img.shields.io/pypi/pyversions/cursor-eta.svg)](https://pypi.org/project/cursor-eta/)
[![codecov](https://codecov.io/gh/cursor-eta/cursor-eta/branch/main/graph/badge.svg)](https://codecov.io/gh/cursor-eta/cursor-eta)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **lightweight ETA/progress indicator** for Cursor's Agent calls that adds **zero tokens and zero latency** to your LLM requests, while keeping you informed during long-running operations.

## 🚀 Why This Exists

When Cursor's AI agents work on complex tasks, users often wonder:
- How long will this take?
- Is it still running?
- What step is it on?

This tool provides real-time feedback **without adding a single token** to your prompts or affecting response quality.

## 🎯 Key Features

- **Zero Token Overhead**: All tracking happens AFTER the prompt is sent
- **Two Display Modes**:
  - **Console Mode**: Simple progress bar in terminal (works today!)
  - **Status Bar Mode**: VS Code extension for always-visible progress
- **Smart ETA Calculation**: Learns from actual progress to refine estimates
- **Lightweight**: No servers, no databases, just stdio pipes

## 📁 Project Structure

```
cursor-eta-indicator/
├── python/
│   ├── agent_with_eta.py    # Core wrapper with ETA logic
│   └── eta_bridge.py         # Example integration
└── vscode-extension/
    ├── src/
    │   └── extension.ts      # VS Code status bar integration
    ├── package.json          # Extension manifest
    └── tsconfig.json         # TypeScript config
```

## 🚦 Quick Start

### Console Mode (Works Today!)

1. **Run the example:**
   ```bash
   cd python
   python eta_bridge.py "Refactor authentication system" --complexity complex
   ```

2. **Watch the magic:**
   ```
   ETA: 24s | Step 3/9 [██████░░░░░░░░░░░░░░] 33%
   ```

3. **Integrate with your code:**
   ```python
   from agent_with_eta import AgentWrapper
   
   wrapper = AgentWrapper()
   result = wrapper.execute_with_eta(
       your_agent_function,
       eta_total_steps=10,
       eta_expected_duration=30.0
   )
   ```

### Status Bar Mode (VS Code Extension)

1. **Build the extension:**
   ```bash
   cd vscode-extension
   npm install
   npm run compile
   ```

2. **Install locally:**
   - Press `F5` in VS Code to launch a new window with the extension
   - The status bar will show: `⏱ ETA 12s | 3/10`

3. **Configure (optional):**
   - `cursorETA.alignment`: "left" or "right"
   - `cursorETA.priority`: Status bar position priority
   - `cursorETA.hideDelay`: Ms before hiding after completion

## 🔧 How It Works

### The Zero-Token Promise

Traditional progress tracking would require:
```python
# ❌ BAD: Adds tokens to every request
prompt = f"Current step: {step}. Please continue and update progress..."
```

Our approach:
```python
# ✅ GOOD: Tracking happens AFTER prompt submission
send_prompt_to_llm(prompt)  # No progress info included!
tracker.start()             # Begin tracking separately
```

### Architecture

```
[Your Code] → [agent_with_eta.py] → [LLM API]
                    ↓
              [Progress Updates]
                    ↓
         [Console] or [VS Code Status Bar]
```

1. **Python Wrapper** intercepts agent calls
2. **Background Thread** emits progress updates via stdout
3. **Display Layer** (console or VS Code) shows updates
4. **No LLM Impact** - all tracking is client-side only

## 📊 Output Format

The wrapper emits two types of output:

1. **Human-readable** (stderr):
   ```
   ETA: 1m 24s | Step 3/10 [██████░░░░░░░░░░░░░░] 30%
   ```

2. **Machine-readable** (stdout):
   ```
   STATUS|{"eta_seconds": 84, "current_step": 3, "total_steps": 10, ...}
   ```

## 🎨 Customization

### Python Wrapper Options

```python
wrapper.execute_with_eta(
    func,
    eta_total_steps=10,        # Expected number of steps
    eta_expected_duration=30,  # Expected duration in seconds
    eta_expected_tokens=1000   # Expected token usage (optional)
)
```

### VS Code Extension Settings

```json
{
  "cursorETA.enabled": true,
  "cursorETA.alignment": "left",
  "cursorETA.priority": 100,
  "cursorETA.hideDelay": 5000
}
```

## 🧪 Testing

Run the test suite:
```bash
cd python
python -m pytest test_agent_eta.py -v
```

Try different complexity levels:
```bash
python eta_bridge.py "Simple task" --complexity simple
python eta_bridge.py "Medium task" --complexity medium  
python eta_bridge.py "Complex task" --complexity complex
```

## 🤝 Integration Examples

### With Cursor's Agent API

```python
from agent_with_eta import AgentWrapper

wrapper = AgentWrapper()

def my_cursor_agent_task():
    # Your existing agent code
    wrapper.update_step(1, "Analyzing codebase")
    # ... analysis logic ...
    
    wrapper.update_step(2, "Generating changes")
    # ... generation logic ...
    
    wrapper.update_tokens(tokens_used)
    
    return results

# Run with tracking
result = wrapper.execute_with_eta(
    my_cursor_agent_task,
    eta_total_steps=5,
    eta_expected_duration=20.0
)
```

### Custom Step Tracking

```python
# Manual step updates
wrapper.update_step(3, "Running tests")

# Automatic increment
wrapper.update_step(description="Validating output")

# Token tracking
wrapper.update_tokens(current_token_count)
```

## 🚧 Roadmap

- [x] Console progress output
- [x] VS Code status bar extension
- [x] Smart ETA calculation
- [ ] WebView task monitor (stretch goal)
- [ ] Historical timing data
- [ ] Multi-task tracking
- [ ] Progress notifications

## 💡 Why No Token Cost?

This tool operates on a simple principle: **separation of concerns**.

- **LLM's job**: Generate the best possible response
- **Our job**: Show progress while waiting

By keeping these separate, we get progress tracking "for free" - no prompt engineering, no output parsing, no token waste.

## 📝 License

MIT License - Use freely in your Cursor workflows!

## 🙏 Contributing

PRs welcome! Key areas:
- Better terminal detection for auto-attachment
- More sophisticated ETA algorithms
- Additional display modes
- Integration examples

---

**Remember**: The best progress indicator is one that costs zero tokens! 🎯