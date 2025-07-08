# Cursor-ETA ‑ Know When the Agent Finishes

Cursor-ETA shows a live *≈ETA* timer and progress bar for long-running Cursor AI agent runs. It adds **zero token overhead** and works both in the terminal and through an optional VS Code status-bar extension.

---

## Features
* Real-time ETA (seconds / minutes / hours)
* Progress bar with **current step / total steps**
* Live token counter
* JSON `STATUS|…` messages for machine consumption (used by the VS Code extension)
* Decorator `@track_agent` for one-liner integration
* Pure-Python, **no external dependencies**

---

## Quick Start
```bash
# 1. Install from source (PyPI publication coming later)
pip install -e cursor-eta-indicator

# 2. Use in your agent code
from cursor_eta import track_agent

@track_agent(steps=5, duration=20.0)
def my_agent():
    ...

my_agent()

# 3. Optional – show status in VS Code
a) cd cursor-eta-indicator/vscode-extension
b) npm install && npm run package
c) code --install-extension cursor-eta-*.vsix
```

Run the built-in demo:
```bash
python -m cursor_eta --demo
```

---

## How It Works
```mermaid
graph LR
    A[Your Agent Code] --decorated--> B[AgentWrapper.execute_with_eta]
    B --> C[AgentETATracker.start]
    C --> D[Background Update Thread]
    D --> E{{\"STATUS|{…}\" on stdout}}
    D --> F[/ETA line on stderr/]
    E -->|Parse| G[VS Code Extension]
```
* The tracker starts a background thread that emits human-readable updates to `stderr` and machine-readable JSON to `stdout`.
* The VS Code extension listens for `STATUS|…` lines and shows a status-bar item.

---

## Roadmap / Known Limitations
1. **Dynamic Token Rate** – current ETA assumes linear token-per-second throughput; spiky model latency can skew early estimates.
2. **Branchy Agents** – adding new steps on the fly will stretch ETA; we plan adaptive re-estimation.
3. **PyPI Release** – publish `cursor-eta` once the API stabilises.
4. **Native Cursor Integration** – auto-inject wrapper without env-vars.

---

## License
MIT © Cursor ETA Contributors
