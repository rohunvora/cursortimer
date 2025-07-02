ETA-Timer for Cursor - Know When Your Coffee Is Safe

What it does
Slaps a live “≈ETA xx s” read-out on your Cursor Agent runs so you can walk away without gambling on how long the LLM will churn.

Why you should care

Pain	How ETA-Timer fixes it
Blind waits – You launch an Agent run and have no clue if it’ll finish before your screen locks.	One-line countdown right in the Agent panel (or status-bar widget if you install the VS Code extension).
Interrupt anxiety – You hover, wondering if killing the run will save time or waste more.	Live progress (tokens generated, steps remaining) tells you whether to bail or grab water.
Wasted tokens for “progress” chatter – Asking the model itself to predict time burns tokens and is wrong anyway.	Timing happens outside the LLM, so token cost = 0.


⸻

Quick install (60 s)

# 1. drop the Python wrapper somewhere in your repo
curl -o .cursor/eta_wrapper.py https://raw.githubusercontent.com/you/eta-timer/main/eta_wrapper.py

# 2. tell Cursor to use it
export CURSOR_AGENT_WRAPPER=".cursor/eta_wrapper.py"

# 3. (optional) VS Code status-bar bling
code --install-extension eta-timer-statusbar.vsix

No rebuilds, no system-prompt hacks, no extra OpenAI params. Done.

⸻

What you’ll see

≈ETA 18 s | 1/2 steps | 0/900 tok
 5s elapsed | 430/900 tok | ≈9 s left
✅ Done in 15 s | 2 edits, 1 test pass

In the GUI: a slim status-bar item mirrors the same text; hover for a fuller breakdown.

⸻

How it works (in plain English)
	1.	Counts tokens before the call.
tiktoken tells us how many input tokens we’re sending and guesses output length (1.1× heuristic).
	2.	Divides by the rolling median TPS you hit on this model tier (captured automatically after each run).
	3.	Prints + rewrites a single console line every second using \r. Cursor’s Agent panel auto-refreshes it.
	4.	Optional VS Code extension reads those lines and rewires them into a status-bar widget. No sockets; just standard stdin.

Zero tokens, zero latency overhead, no apology-spam from the model.

⸻

Configuration knobs

Env Var / Flag	Default	What it does
ETA_TPS_DEFAULT	60	Fallback tokens-per-second for the first run on a new engine.
ETA_FILE_STEP_SEC	0.5	Assumed cost of each Planner/Executor file-edit or test step.
ETA_NOTIFY_THRESHOLD_SEC	30	If ETA > threshold, sends a desktop notification and hides the timer.

Edit these in eta_wrapper.py or export them from your shell rc.

⸻

Caveats (don’t say we didn’t warn you)
	•	Queue spikes: If OpenAI throttles, first token can get stuck. Timer corrects once streaming begins, but initial ETA may be optimistic.
	•	Branchy agents: If your Planner suddenly spawns five extra calls, ETA stretches. Wrapper updates every step, but expect jumps.
	•	Local models: TPS varies with thermals; let a few runs collect before trusting numbers.

⸻

Uninstall

rm .cursor/eta_wrapper.py
unset CURSOR_AGENT_WRAPPER
code --uninstall-extension eta-timer-statusbar

That’s it—Cursor goes back to silent treatments.

⸻

License

MIT. Fork it, rip it apart, tattoo it on your dog—whatever.

⸻

Stop hovering, start timing.
