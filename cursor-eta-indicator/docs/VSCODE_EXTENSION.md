# VS Code Extension Guide

Complete guide for the Cursor ETA Indicator VS Code extension.

## 📦 Installation

### From Open VSX Registry

```bash
code --install-extension cursor-eta.cursor-eta
```

### From VS Code Marketplace

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "Cursor ETA Indicator"
4. Click "Install"

### Manual Installation

1. Download the latest `.vsix` file from [releases](https://github.com/yourusername/cursor-eta-indicator/releases)
2. Install via command line:
   ```bash
   code --install-extension cursor-eta-*.vsix
   ```
3. Or install via VS Code:
   - Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
   - Run "Extensions: Install from VSIX..."
   - Select the downloaded `.vsix` file

## 🎯 Features

### Status Bar Integration

The extension adds a real-time ETA indicator to your VS Code status bar:

- **Progress Display**: Shows current step and total steps
- **ETA Calculation**: Displays estimated time remaining
- **Token Tracking**: Monitor AI token consumption
- **Customizable Format**: Configure the display format

### Commands

The extension provides several commands accessible via Command Palette:

| Command | Description |
|---------|-------------|
| `Cursor ETA: Show Details` | Open detailed progress information |
| `Cursor ETA: Toggle Display` | Show/hide the status bar indicator |
| `Cursor ETA: Reset` | Reset current tracking session |

### Real-time Updates

The extension receives updates from Python scripts via:
- **Standard Output Parsing**: Monitors `ETA_UPDATE:` messages
- **JSON Protocol**: Structured data for progress, errors, and completion
- **System Monitoring**: Automatic CPU and memory usage tracking

## ⚙️ Configuration

Configure the extension through VS Code settings:

### Basic Settings

```json
{
  "cursorETA.enabled": true,
  "cursorETA.showTokens": true,
  "cursorETA.alignment": "left",
  "cursorETA.priority": 100
}
```

### Advanced Settings

```json
{
  "cursorETA.format": "$(clock) ETA: {eta} | Step {current}/{total}",
  "cursorETA.hideDelay": 5000,
  "cursorETA.showPercentage": true,
  "cursorETA.colorizeProgress": true
}
```

## 🎨 Format String Variables

Customize the status bar display using these variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `{eta}` | Estimated time remaining | `2m 30s` |
| `{current}` | Current step number | `3` |
| `{total}` | Total number of steps | `10` |
| `{percent}` | Progress percentage | `30%` |
| `{tokens}` | Tokens consumed | `450` |
| `{description}` | Current step description | `Analyzing code` |

### Format Examples

```json
{
  "cursorETA.format": "$(clock) {eta} | {current}/{total} ({percent})"
}
```
Result: `⏰ 1m 45s | 3/10 (30%)`

```json
{
  "cursorETA.format": "ETA: {eta} | {description}"
}
```
Result: `ETA: 1m 45s | Analyzing codebase`

```json
{
  "cursorETA.format": "Progress: {current}/{total} | Tokens: {tokens}"
}
```
Result: `Progress: 3/10 | Tokens: 450`

## 🔧 Integration with Python

### Basic Integration

```python
from cursor_eta import ETABridge

with ETABridge() as bridge:
    bridge.send_update({
        "type": "start",
        "total_steps": 5,
        "description": "Starting task"
    })
    
    # ... work happens here ...
    
    bridge.send_update({
        "type": "progress",
        "current": 3,
        "total": 5,
        "description": "Processing data",
        "eta": 30.5
    })
```

### Update Message Types

#### Start Message
```json
{
  "type": "start",
  "total_steps": 10,
  "description": "Task description",
  "estimated_duration": 60.0
}
```

#### Progress Message
```json
{
  "type": "progress",
  "current": 3,
  "total": 10,
  "description": "Current step description",
  "eta": 45.2,
  "progress_percent": 30.0,
  "tokens": 150
}
```

#### Error Message
```json
{
  "type": "error",
  "description": "Error occurred",
  "error_message": "Connection timeout",
  "current": 3,
  "total": 10
}
```

#### Complete Message
```json
{
  "type": "complete",
  "description": "Task completed successfully",
  "duration": 65.3,
  "total_tokens": 500
}
```

#### System Message
```json
{
  "type": "system",
  "cpu_percent": 85.2,
  "memory_percent": 67.1,
  "timestamp": 1703123456.789
}
```

## 🎭 UI Behavior

### Status Bar States

1. **Idle**: No indicator visible
2. **Starting**: "Starting..." with spinner
3. **In Progress**: Live ETA and progress updates
4. **Error**: Red indicator with error message
5. **Complete**: Green checkmark, auto-hides after delay

### Visual Indicators

- **Progress Colors**:
  - 🔵 Blue: Normal progress
  - 🟡 Yellow: High resource usage
  - 🔴 Red: Errors or warnings
  - 🟢 Green: Completion

- **Icons**:
  - `$(clock)`: Default ETA icon
  - `$(loading~spin)`: Processing
  - `$(check)`: Completed
  - `$(error)`: Error state
  - `$(warning)`: Warning state

### Tooltips

Hover over the status bar item to see detailed information:
- Full step description
- Exact ETA calculation
- Token usage details
- System resource usage

## 🔍 Troubleshooting

### Common Issues

#### Extension Not Showing

1. **Check if enabled**:
   ```json
   {
     "cursorETA.enabled": true
   }
   ```

2. **Reload VS Code**:
   - Press `Ctrl+Shift+P` / `Cmd+Shift+P`
   - Run "Developer: Reload Window"

3. **Check Output Panel**:
   - View → Output
   - Select "Cursor ETA" from dropdown

#### No Updates Received

1. **Verify Python script output**:
   ```python
   print("ETA_UPDATE:" + json.dumps(update_data), flush=True)
   ```

2. **Check console output** in VS Code Developer Tools:
   - Help → Toggle Developer Tools
   - Look for console errors

3. **Test with simple update**:
   ```bash
   echo 'ETA_UPDATE:{"type":"start","total_steps":1}'
   ```

#### Performance Issues

1. **Reduce update frequency** in Python code
2. **Disable token tracking** if not needed:
   ```json
   {
     "cursorETA.showTokens": false
   }
   ```
3. **Increase hide delay**:
   ```json
   {
     "cursorETA.hideDelay": 10000
   }
   ```

### Debug Mode

Enable debug logging:

```json
{
  "cursorETA.debug": true
}
```

This will log all received messages to the Output panel.

## 🧪 Testing the Extension

### Manual Testing

1. **Install locally**:
   ```bash
   cd vscode-extension
   npm install
   npm run compile
   code --install-extension .
   ```

2. **Test with Python**:
   ```python
   from cursor_eta import ETABridge
   
   with ETABridge() as bridge:
       bridge.send_update({"type": "start", "total_steps": 3})
       # Should see status bar update
   ```

3. **Test commands**:
   - Open Command Palette
   - Search "Cursor ETA"
   - Test each command

### Development Testing

1. **Launch extension host**:
   - Open `vscode-extension` folder in VS Code
   - Press `F5` to launch new VS Code window with extension

2. **Debug output**:
   - Use `console.log()` in TypeScript code
   - View in Developer Tools console

3. **Breakpoints**:
   - Set breakpoints in TypeScript code
   - Debug with VS Code debugger

## 📚 API Reference

### Extension Commands

- `cursorETA.showDetails`
- `cursorETA.toggle`
- `cursorETA.reset`

### Configuration Properties

- `cursorETA.enabled`: boolean
- `cursorETA.showTokens`: boolean
- `cursorETA.format`: string
- `cursorETA.alignment`: "left" | "right"
- `cursorETA.priority`: number
- `cursorETA.hideDelay`: number

### Events

The extension listens for:
- Python process output containing `ETA_UPDATE:`
- System resource threshold events
- VS Code workspace changes

## 🔗 Related Resources

- [Python API Documentation](API_REFERENCE.md)
- [Basic Usage Examples](../examples/basic_usage.py)
- [VS Code Integration Examples](../examples/vscode_integration.py)
- [CI Pipeline Documentation](CI_PIPELINE.md)