# Changelog

All notable changes to cursor-eta will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial release of cursor-eta
- Python wrapper (`AgentETATracker` and `AgentWrapper` classes) for zero-overhead progress tracking
- Real-time ETA calculation based on step progress
- Console mode with live-updating progress bar
- Machine-readable JSON status output for integration with VS Code extension
- `@track_agent` decorator for easy integration
- Command-line interface (`cursor-eta` command)
- Demo mode to showcase functionality
- Full type hints for better IDE support
- Comprehensive test suite
- PyPI package structure with modern `pyproject.toml`

### Features
- **Zero Token Overhead**: All tracking happens after LLM prompt submission
- **Dual Output**: Human-readable progress (stderr) and machine-readable status (stdout)
- **Smart ETA**: Adaptive calculation based on actual progress vs expected duration
- **Token Tracking**: Monitor token usage during agent operations
- **Thread-Safe**: Background updates don't interfere with main execution

### Documentation
- Comprehensive README with quick-start guide
- API documentation in docstrings
- Example usage patterns
- VS Code integration guide

[0.1.0]: https://github.com/cursor-eta/cursor-eta/releases/tag/v0.1.0