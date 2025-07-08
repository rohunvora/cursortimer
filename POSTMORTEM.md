# Cursor-ETA Post-Mortem

## 1. Original Goal
Provide developers using Cursor AI with a live ETA/progress indicator that costs *zero* additional model tokens and can be surfaced both in the terminal and inside VS Code.

## 2. Status Quo Ante
* Core tracker and wrapper classes were implemented and well-tested.
* A VS Code extension stub displayed simulated updates.
* README was a rough brainstorm document.
* Edge-case tests (`total_steps = 0`) failed due to division-by-zero.
* Packaging version was still `0.1.0` and merge was unfinished.

## 3. What Blocked Completion
1. **Edge-Cases Unhandled** – division by zero when `total_steps == 0` broke tests.
2. **Docs Debt** – README read like an internal pitch deck, not user-facing docs.
3. **Unfinished Merge** – repo was mid-merge, preventing a clean release.

## 4. Decisions Made for v1.0.1
| Area | Decision |
|------|----------|
| Robustness | Guard against `total_steps <= 0` in `get_eta()` and `get_status()`; return graceful defaults. |
| Versioning | Bumped package to `0.1.1` to signal bug-fix release. |
| Documentation | Rewrote README for clarity; added architecture Mermaid diagram and roadmap. |
| Transparency | Added this `POSTMORTEM.md` to capture context for future maintainers. |

## 5. Future Improvements
1. **Adaptive ETA** – adjust remaining time based on recent throughput instead of linear extrapolation.
2. **Native Cursor Integration** – auto-wrap agent without env-vars; emit status directly to Cursor panel API when available.
3. **Extension Polishing** – replace simulated data with real stdout parsing; add cmd-palette commands.
4. **CI & Release** – add GitHub Actions to run tests, linters, and publish to PyPI on tag.
5. **PyPI & VSIX Distribution** – automate publishing of both Python package and VS Code extension.

---
MIT © Cursor ETA Contributors 