# Cursor ETA Indicator

[![PyPI version](https://badge.fury.io/py/cursor-eta.svg)](https://badge.fury.io/py/cursor-eta)
[![CI](https://github.com/yourusername/cursor-eta-indicator/workflows/CI/badge.svg)](https://github.com/yourusername/cursor-eta-indicator/actions)
[![Coverage](https://codecov.io/gh/yourusername/cursor-eta-indicator/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/cursor-eta-indicator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Real-time ETA and progress indicators for Cursor AI agent operations. Track progress, monitor performance, and get accurate time estimates for your AI-powered coding tasks.

## 🚀 Features

- **Real-time Progress Tracking**: Visual progress bars and step-by-step updates
- **Accurate ETA Calculations**: Machine learning-based time estimation
- **Token Usage Monitoring**: Track AI token consumption in real-time
- **VS Code Integration**: Native status bar indicators and notifications
- **Python API**: Easy integration into any Python project
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Lightweight**: Minimal overhead, maximum insight

## 📦 Installation

### Python Package

```bash
pip install cursor-eta
```

### VS Code Extension

1. **From Open VSX Registry**:
   ```bash
   code --install-extension cursor-eta.cursor-eta
   ```

2. **From VS Code Marketplace** (if published):
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Cursor ETA Indicator"
   - Click Install

3. **Manual Installation**:
   - Download the latest `.vsix` file from [releases](https://github.com/yourusername/cursor-eta-indicator/releases)
   - Run: `code --install-extension cursor-eta-*.vsix`

## 🎯 Quick Start

### Python API

```python
import time
from cursor_eta import AgentWrapper

# Create a wrapper instance
wrapper = AgentWrapper()

def my_ai_task():
    """Simulate an AI coding task."""
    for i in range(5):
        wrapper.update_step(i + 1, f"Processing step {i + 1}")
        time.sleep(1)  # Simulate work
        
        # Update token usage
        if i % 2 == 0:
            wrapper.update_tokens(100 * (i + 1))
    
    return "Task completed!"

# Execute with ETA tracking
result = wrapper.execute_with_eta(
    my_ai_task,
    eta_total_steps=5,
    eta_expected_duration=10.0,
    eta_expected_tokens=500
)

print(result)
```

### Decorator Syntax

```python
from cursor_eta import track_agent
import time

@track_agent(steps=3, duration=5.0, tokens=300)
def process_files():
    """Process files with automatic ETA tracking."""
    files = ["main.py", "utils.py", "config.json"]
    
    for i, filename in enumerate(files, 1):
        print(f"Processing {filename}...")
        time.sleep(1.5)  # Simulate processing
    
    return f"Processed {len(files)} files"

result = process_files()
```

### CLI Usage

```bash
# Run a demo
cursor-eta demo

# Check installation
cursor-eta check

# Show help
cursor-eta help

# Show version
cursor-eta version
```

## 🎮 VS Code Extension Usage

Once installed, the extension automatically:

1. **Shows Progress in Status Bar**: Real-time ETA and step information
2. **Displays Token Usage**: Monitor AI token consumption
3. **Provides Commands**:
   - `Cursor ETA: Show Details` - Detailed progress information
   - `Cursor ETA: Toggle Display` - Show/hide the status bar
   - `Cursor ETA: Reset` - Reset current tracking

### Configuration

Configure the extension in VS Code settings:

```json
{
    "cursorETA.enabled": true,
    "cursorETA.showTokens": true,
    "cursorETA.format": "$(clock) ETA: {eta} | Step {current}/{total}",
    "cursorETA.alignment": "left",
    "cursorETA.priority": 100
}
```

## 📖 Documentation

- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[VS Code Extension Guide](docs/VSCODE_EXTENSION.md)** - Extension features and configuration
- **[Examples](examples/)** - Real-world usage examples
- **[Contributing](CONTRIBUTING.md)** - Development and contribution guide
- **[CI Pipeline](docs/CI_PIPELINE.md)** - CI/CD documentation

## 🔧 Advanced Usage

### Custom ETA Calculations

```python
from cursor_eta import AgentETATracker

# Create a custom tracker
tracker = AgentETATracker(
    total_steps=10,
    expected_duration=30.0
)

tracker.start(tokens_expected=1000)

# Manual step updates
tracker.step(3, "Analyzing codebase")
tracker.update_tokens(250)

# Get current status
status = tracker.get_status()
print(f"ETA: {status['eta_seconds']}s")
print(f"Progress: {status['progress_percent']}%")

tracker.stop()
```

### Integration with VS Code

```python
from cursor_eta import ETABridge

# Bridge for VS Code communication
with ETABridge() as bridge:
    bridge.send_update({
        "type": "progress",
        "current": 3,
        "total": 10,
        "description": "Processing files",
        "eta": 15.5
    })
```

## 🏗️ Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/cursor-eta-indicator.git
cd cursor-eta-indicator

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest --cov=cursor_eta

# Run linting
tox -e lint
```

### VS Code Extension Development

```bash
cd vscode-extension

# Install dependencies
npm ci

# Compile TypeScript
npm run compile

# Package extension
npm run package
```

### Running Tests

```bash
# Python tests
pytest tests/ -v

# With coverage
pytest --cov=cursor_eta --cov-report=html

# Multiple Python versions
tox

# Pre-commit checks
pre-commit run --all-files
```

## � Performance

- **Overhead**: < 1ms per update
- **Memory Usage**: < 5MB additional memory
- **CPU Impact**: Negligible background monitoring
- **Token Tracking**: Real-time with no API calls

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📋 Requirements

- **Python**: 3.8+ (for Python package)
- **VS Code**: 1.74.0+ (for extension)
- **Node.js**: 18+ (for extension development)

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install cursor-eta --upgrade
   ```

2. **VS Code Extension Not Working**
   - Check if extension is enabled
   - Reload VS Code window
   - Check output panel for errors

3. **Performance Issues**
   - Reduce update frequency
   - Disable token tracking if not needed

4. **Type Checking Issues**
   ```bash
   pip install types-psutil
   ```

For more issues, check our [GitHub Issues](https://github.com/yourusername/cursor-eta-indicator/issues).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Cursor Team** - For the amazing AI coding assistant
- **VS Code Team** - For the excellent extension API
- **Contributors** - For making this project better

## 🔗 Links

- [PyPI Package](https://pypi.org/project/cursor-eta/)
- [VS Code Extension](https://open-vsx.org/extension/cursor-eta/cursor-eta)
- [GitHub Repository](https://github.com/yourusername/cursor-eta-indicator)
- [Documentation](https://cursor-eta.github.io)
- [Bug Reports](https://github.com/yourusername/cursor-eta-indicator/issues)

---

**Made with ❤️ for the Cursor community**