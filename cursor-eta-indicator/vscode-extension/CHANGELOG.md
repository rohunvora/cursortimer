# Changelog

All notable changes to the Cursor ETA Indicator extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-01-02

### Added
- Initial release of Cursor ETA Indicator
- Real-time ETA display in status bar
- Progress tracking with step indicators
- Token usage monitoring
- Configurable display format and position
- Commands for show details, toggle display, and reset
- Auto-hide after completion with configurable delay
- Support for custom format strings
- Dark theme icon and gallery banner

### Features
- Zero overhead tracking - no impact on AI operations
- Automatic detection of wrapped Python processes
- Live updates via stdio communication
- Customizable status bar format with variables
- Cross-platform support (Windows, macOS, Linux)

### Configuration
- `cursorETA.enabled` - Enable/disable the extension
- `cursorETA.alignment` - Status bar position (left/right)
- `cursorETA.priority` - Status bar priority
- `cursorETA.hideDelay` - Auto-hide delay in milliseconds
- `cursorETA.showTokens` - Show/hide token usage
- `cursorETA.format` - Custom format string

[Unreleased]: https://github.com/yourusername/cursor-eta-indicator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/cursor-eta-indicator/releases/tag/v0.1.0