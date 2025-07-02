# Cursor ETA Indicator

Real-time ETA and progress indicators for Cursor AI agent operations.

## Features

- **Live Progress Tracking**: See real-time progress of Cursor AI operations
- **ETA Display**: Know approximately when operations will complete
- **Token Usage**: Monitor token consumption during operations
- **Zero Overhead**: All tracking happens outside the AI context
- **Customizable**: Configure display format, position, and behavior

## How It Works

This extension works by monitoring Python processes that use the `cursor-eta` wrapper. When a wrapped AI operation runs, it:

1. Captures progress updates via stdio communication
2. Displays ETA and progress in the VS Code status bar
3. Updates in real-time without impacting the AI operation

## Installation

### From Open VSX Registry

```bash
code --install-extension cursor-eta.cursor-eta
```

### From VSIX file

1. Download the `.vsix` file from [Releases](https://github.com/yourusername/cursor-eta-indicator/releases)
2. Install: `code --install-extension cursor-eta-*.vsix`

## Usage

### Basic Usage

1. Install the Python wrapper:
   ```bash
   pip install cursor-eta
   ```

2. Wrap your Cursor operations:
   ```python
   from cursor_eta import track_agent
   
   @track_agent(steps=10, duration=30.0)
   def my_cursor_task():
       # Your Cursor AI operation
       pass
   ```

3. The extension automatically detects and displays progress

### Status Bar Display

The status bar shows:
- Current ETA (time remaining)
- Step progress (e.g., 3/10)
- Current operation description
- Token usage (optional)

### Commands

- **Show Cursor ETA Details**: Display detailed progress information
- **Toggle Cursor ETA Display**: Show/hide the status bar indicator
- **Reset Cursor ETA**: Clear current tracking state

## Configuration

Configure in VS Code settings (`Ctrl+,` or `Cmd+,`):

| Setting | Description | Default |
|---------|-------------|---------|
| `cursorETA.enabled` | Enable/disable the extension | `true` |
| `cursorETA.alignment` | Status bar position (left/right) | `left` |
| `cursorETA.priority` | Status bar priority | `100` |
| `cursorETA.hideDelay` | Hide delay after completion (ms) | `5000` |
| `cursorETA.showTokens` | Show token usage | `true` |
| `cursorETA.format` | Custom format string | `$(clock) ETA: {eta} \| Step {current}/{total}` |

### Format String Variables

- `{eta}` - Estimated time remaining
- `{current}` - Current step number
- `{total}` - Total steps
- `{percent}` - Progress percentage
- `{tokens}` - Token usage
- `{description}` - Current step description

## Requirements

- VS Code 1.74.0 or higher
- Python 3.8+ with `cursor-eta` package installed
- Active Cursor AI operations using the wrapper

## Troubleshooting

### Status bar not showing

1. Check that the extension is enabled in settings
2. Verify `cursor-eta` Python package is installed
3. Ensure your code uses the wrapper decorators

### No progress updates

1. Check that the Python process is running
2. Verify stdio communication is not blocked
3. Check VS Code Developer Tools console for errors

## Contributing

Contributions welcome! Please see our [Contributing Guide](https://github.com/yourusername/cursor-eta-indicator/blob/main/CONTRIBUTING.md).

## License

MIT - see [LICENSE](https://github.com/yourusername/cursor-eta-indicator/blob/main/LICENSE) for details.