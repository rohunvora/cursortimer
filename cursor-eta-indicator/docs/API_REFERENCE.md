# API Reference

Complete API documentation for the Cursor ETA Indicator package.

## Table of Contents

- [AgentETATracker](#agenteta-tracker)
- [AgentWrapper](#agentwrapper)
- [ETABridge](#etabridge)
- [Decorators](#decorators)
- [Type Definitions](#type-definitions)

## AgentETATracker

The core class for tracking progress and calculating ETAs.

### Constructor

```python
AgentETATracker(total_steps: int, expected_duration: float = 60.0)
```

**Parameters:**
- `total_steps` (int): Total number of steps in the task
- `expected_duration` (float, optional): Expected duration in seconds. Default: 60.0

**Example:**
```python
from cursor_eta import AgentETATracker

tracker = AgentETATracker(total_steps=10, expected_duration=30.0)
```

### Methods

#### start()

```python
start(tokens_expected: Optional[int] = None) -> None
```

Start tracking progress.

**Parameters:**
- `tokens_expected` (int, optional): Expected number of tokens to be consumed

**Example:**
```python
tracker.start(tokens_expected=1000)
```

#### stop()

```python
stop() -> None
```

Stop tracking and finalize timing data.

**Example:**
```python
tracker.stop()
```

#### step()

```python
step(step_number: Optional[int] = None, description: str = "") -> None
```

Update the current step.

**Parameters:**
- `step_number` (int, optional): Specific step number. If None, auto-increments
- `description` (str, optional): Description of the current step

**Example:**
```python
tracker.step(3, "Analyzing codebase")
tracker.step(description="Processing files")  # Auto-increment
```

#### update_tokens()

```python
update_tokens(tokens_used: int) -> None
```

Update the number of tokens consumed.

**Parameters:**
- `tokens_used` (int): Total tokens used so far

**Example:**
```python
tracker.update_tokens(500)
```

#### get_eta()

```python
get_eta() -> float
```

Get the estimated time remaining in seconds.

**Returns:**
- `float`: Estimated seconds remaining

**Example:**
```python
eta = tracker.get_eta()
print(f"ETA: {eta:.1f} seconds")
```

#### get_status()

```python
get_status() -> Dict[str, Any]
```

Get comprehensive status information.

**Returns:**
- `Dict[str, Any]`: Status dictionary with keys:
  - `current_step` (int): Current step number
  - `total_steps` (int): Total number of steps
  - `progress_percent` (float): Progress percentage (0-100)
  - `eta_seconds` (float): Estimated seconds remaining
  - `eta_formatted` (str): Human-readable ETA
  - `current_description` (str): Current step description
  - `tokens_used` (int): Tokens consumed so far
  - `tokens_expected` (int): Expected total tokens
  - `elapsed_time` (float): Elapsed time in seconds
  - `is_running` (bool): Whether tracking is active

**Example:**
```python
status = tracker.get_status()
print(f"Progress: {status['progress_percent']:.1f}%")
print(f"ETA: {status['eta_formatted']}")
```

### Properties

#### is_running

```python
@property
is_running -> bool
```

Whether the tracker is currently running.

#### total_steps

```python
@property
total_steps -> int
```

Total number of steps in the task.

#### current_step

```python
@property
current_step -> int
```

Current step number.

## AgentWrapper

High-level wrapper for executing functions with ETA tracking.

### Constructor

```python
AgentWrapper()
```

**Example:**
```python
from cursor_eta import AgentWrapper

wrapper = AgentWrapper()
```

### Methods

#### execute_with_eta()

```python
execute_with_eta(
    func: Callable,
    *args,
    eta_total_steps: int = 5,
    eta_expected_duration: float = 30.0,
    eta_expected_tokens: Optional[int] = None,
    **kwargs
) -> Any
```

Execute a function with automatic ETA tracking.

**Parameters:**
- `func` (Callable): Function to execute
- `*args`: Positional arguments for the function
- `eta_total_steps` (int, optional): Total number of steps. Default: 5
- `eta_expected_duration` (float, optional): Expected duration in seconds. Default: 30.0
- `eta_expected_tokens` (int, optional): Expected token consumption
- `**kwargs`: Keyword arguments for the function

**Returns:**
- `Any`: Return value of the executed function

**Example:**
```python
def my_task():
    # Task implementation
    return "completed"

result = wrapper.execute_with_eta(
    my_task,
    eta_total_steps=10,
    eta_expected_duration=60.0,
    eta_expected_tokens=1000
)
```

#### update_step()

```python
update_step(step_number: Optional[int] = None, description: str = "") -> None
```

Update the current step. Can only be called during `execute_with_eta()`.

**Parameters:**
- `step_number` (int, optional): Specific step number
- `description` (str, optional): Step description

**Example:**
```python
def my_task():
    wrapper.update_step(1, "Starting analysis")
    # ... work ...
    wrapper.update_step(2, "Processing data")
    # ... work ...
    return "done"

wrapper.execute_with_eta(my_task, eta_total_steps=3)
```

#### update_tokens()

```python
update_tokens(tokens_used: int) -> None
```

Update token consumption. Can only be called during `execute_with_eta()`.

**Parameters:**
- `tokens_used` (int): Total tokens used

**Example:**
```python
def my_task():
    # ... work ...
    wrapper.update_tokens(250)
    # ... more work ...
    wrapper.update_tokens(500)
    return "done"

wrapper.execute_with_eta(my_task)
```

## ETABridge

Bridge for communication with VS Code extension.

### Constructor

```python
ETABridge()
```

**Example:**
```python
from cursor_eta import ETABridge

bridge = ETABridge()
```

### Methods

#### start()

```python
start() -> None
```

Start the bridge and begin system monitoring.

#### stop()

```python
stop() -> None
```

Stop the bridge and end monitoring.

#### send_update()

```python
send_update(update: Dict[str, Any]) -> None
```

Send an update to the VS Code extension.

**Parameters:**
- `update` (Dict[str, Any]): Update data to send

**Example:**
```python
bridge.send_update({
    "type": "progress",
    "current": 3,
    "total": 10,
    "description": "Processing files",
    "eta": 15.5
})
```

### Context Manager Usage

```python
with ETABridge() as bridge:
    bridge.send_update({"type": "start", "total_steps": 5})
    # Bridge automatically stopped when exiting context
```

## Decorators

### track_agent()

```python
track_agent(
    steps: int = 5,
    duration: float = 30.0,
    tokens: Optional[int] = None
) -> Callable
```

Decorator for automatic ETA tracking.

**Parameters:**
- `steps` (int, optional): Total number of steps. Default: 5
- `duration` (float, optional): Expected duration in seconds. Default: 30.0
- `tokens` (int, optional): Expected token consumption

**Example:**
```python
from cursor_eta import track_agent

@track_agent(steps=3, duration=10.0, tokens=500)
def process_data():
    # Function implementation
    return "processed"

result = process_data()
```

## Type Definitions

### StatusDict

```python
class StatusDict(TypedDict):
    current_step: int
    total_steps: int
    progress_percent: float
    eta_seconds: float
    eta_formatted: str
    current_description: str
    tokens_used: int
    tokens_expected: int
    elapsed_time: float
    is_running: bool
```

### UpdateDict

```python
class UpdateDict(TypedDict, total=False):
    type: str
    current: int
    total: int
    description: str
    eta: float
    tokens: int
    timestamp: float
```

## Error Handling

### Common Exceptions

#### ValueError

Raised when invalid parameters are provided:

```python
# Invalid step number
tracker.step(-1)  # Raises ValueError

# Invalid total steps
AgentETATracker(total_steps=0)  # Raises ValueError
```

#### RuntimeError

Raised when operations are called in wrong state:

```python
# Calling update_step outside of execute_with_eta
wrapper.update_step(1)  # Raises RuntimeError

# Starting already running tracker
tracker.start()
tracker.start()  # Raises RuntimeError
```

### Best Practices

1. **Always call stop()**: Use try/finally or context managers

```python
tracker = AgentETATracker(10)
try:
    tracker.start()
    # ... work ...
finally:
    tracker.stop()
```

2. **Handle exceptions in functions**:

```python
def safe_task():
    try:
        wrapper.update_step(1, "Starting")
        # ... potentially failing work ...
        wrapper.update_step(2, "Completing")
    except Exception as e:
        wrapper.update_step(description=f"Error: {e}")
        raise

wrapper.execute_with_eta(safe_task)
```

3. **Check is_running before operations**:

```python
if tracker.is_running:
    tracker.update_tokens(100)
```

## Performance Considerations

- **Update frequency**: Limit updates to avoid overhead
- **Token tracking**: Optional, disable if not needed
- **Step descriptions**: Keep concise for better performance
- **Memory usage**: Tracker stores minimal state

## Thread Safety

- **AgentETATracker**: Thread-safe for read operations
- **AgentWrapper**: Not thread-safe, use one per thread
- **ETABridge**: Thread-safe for all operations

## Version Compatibility

- **Python**: 3.8+
- **Dependencies**: 
  - `psutil>=5.9.0` (optional, for system monitoring)
  - `typing-extensions>=4.0.0` (Python <3.9 only)