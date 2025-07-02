# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [0.1.0] - 2024-01-15

### Added

#### Core Features
- **AgentETATracker**: Core class for tracking progress and calculating ETAs
- **AgentWrapper**: High-level wrapper for executing functions with ETA tracking
- **ETABridge**: Communication bridge between Python and VS Code extension
- **@track_agent**: Decorator for automatic ETA tracking
- **Real-time progress bars**: Console-based progress indicators with ETA
- **Token usage tracking**: Monitor AI token consumption in real-time
- **Smart ETA calculation**: Dynamic time estimation based on actual progress

#### Python Package
- **pip installable**: Available as `cursor-eta` package
- **Python 3.8+ support**: Compatible with Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Type hints**: Full type annotation support with py.typed marker
- **CLI interface**: Command-line tool with demo, check, and help commands

#### VS Code Extension
- **Status bar integration**: Real-time ETA display in VS Code status bar
- **Customizable format**: Configure display format with variables
- **Multiple commands**: Show details, toggle display, reset tracking
- **Configuration options**: Alignment, priority, hide delay, token display
- **System monitoring**: CPU and memory usage tracking
- **Error handling**: Graceful error display and recovery

#### Development Infrastructure
- **Comprehensive CI/CD**: GitHub Actions workflows for testing and publishing
- **Multi-platform testing**: Ubuntu, Windows, macOS across Python versions
- **Code quality tools**: Black, isort, flake8, mypy, bandit integration
- **Pre-commit hooks**: Automatic code formatting and validation
- **Automated publishing**: PyPI and Open VSX registry publishing
- **Documentation**: Complete API reference and usage guides

#### Documentation & Examples
- **Complete README**: Installation, usage, and configuration guide
- **API Reference**: Detailed documentation for all classes and methods
- **VS Code Extension Guide**: Configuration and troubleshooting
- **Usage Examples**: Basic usage, VS Code integration, error handling
- **Contributing Guide**: Development setup and contribution guidelines
- **CI Pipeline Documentation**: Complete CI/CD setup and troubleshooting

#### Testing
- **Unit tests**: Comprehensive test suite with >80% coverage
- **Integration tests**: End-to-end testing of Python + VS Code integration
- **Tox support**: Multi-version Python testing
- **Performance tests**: Overhead and memory usage validation
- **Error handling tests**: Edge cases and failure scenarios

### Technical Details

#### Package Structure
```
cursor-eta-indicator/
├── cursor_eta/              # Main Python package
│   ├── __init__.py         # Package exports and convenience functions
│   ├── agent_with_eta.py   # Core ETA tracking implementation
│   └── eta_bridge.py       # VS Code communication bridge
├── vscode-extension/        # VS Code extension
│   ├── src/extension.ts    # Main extension logic
│   ├── package.json        # Extension manifest
│   └── tsconfig.json       # TypeScript configuration
├── tests/                  # Test suite
├── examples/               # Usage examples
├── docs/                   # Documentation
└── .github/workflows/      # CI/CD pipelines
```

#### Dependencies
- **Python**: psutil>=5.9.0, typing-extensions>=4.0.0 (Python <3.9)
- **VS Code**: 1.74.0+
- **Development**: pytest, black, isort, mypy, flake8, pre-commit, tox

#### Performance Characteristics
- **Overhead**: <1ms per update
- **Memory usage**: <5MB additional memory
- **CPU impact**: Negligible background monitoring
- **Token tracking**: Real-time with no API calls

### Configuration Options

#### Python API
```python
# Basic usage
wrapper = AgentWrapper()
result = wrapper.execute_with_eta(
    my_function,
    eta_total_steps=10,
    eta_expected_duration=60.0,
    eta_expected_tokens=1000
)

# Decorator usage
@track_agent(steps=5, duration=30.0, tokens=500)
def my_task():
    # Task implementation
    pass
```

#### VS Code Extension
```json
{
  "cursorETA.enabled": true,
  "cursorETA.showTokens": true,
  "cursorETA.format": "$(clock) ETA: {eta} | Step {current}/{total}",
  "cursorETA.alignment": "left",
  "cursorETA.priority": 100,
  "cursorETA.hideDelay": 5000
}
```

### Breaking Changes
- None (initial release)

### Migration Guide
- None (initial release)

### Known Issues
- VS Code extension requires manual installation in v0.1.0
- Token tracking requires psutil for optimal performance
- Windows path handling may need adjustment in some environments

### Contributors
- Initial implementation and architecture
- CI/CD pipeline setup
- Documentation and examples
- Testing infrastructure

---

## Release Notes

### v0.1.0 - "Foundation Release"

This is the initial release of Cursor ETA Indicator, providing a solid foundation for progress tracking in AI-powered coding workflows.

**Key Highlights:**
- 🚀 **Ready to use**: pip install cursor-eta
- 📊 **Real-time tracking**: Visual progress bars and ETA calculations
- 🔗 **VS Code integration**: Native status bar indicators
- 🧪 **Thoroughly tested**: >80% code coverage across Python 3.8-3.12
- 📚 **Well documented**: Complete API reference and examples
- 🔧 **Developer friendly**: Easy integration with existing workflows

**Getting Started:**
```bash
pip install cursor-eta
cursor-eta demo  # Try it out!
```

**Next Steps:**
- Install VS Code extension for enhanced experience
- Explore examples/ directory for integration patterns
- Read docs/API_REFERENCE.md for detailed usage
- Join the community and contribute!

---

**Links:**
- [PyPI Package](https://pypi.org/project/cursor-eta/)
- [VS Code Extension](https://open-vsx.org/extension/cursor-eta/cursor-eta)
- [GitHub Repository](https://github.com/yourusername/cursor-eta-indicator)
- [Documentation](https://github.com/yourusername/cursor-eta-indicator/blob/main/README.md)