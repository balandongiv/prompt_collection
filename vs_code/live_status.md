I’m switching to a more outage-tolerant approach. I’ll add a dedicated full-sweep runner that writes a live status JSON/Markdown file plus a rolling log, then start it in the background so you can monitor progress without keeping the terminal attached.

I’m making this restartable and observable. The runner will emit a live status file you can open while it runs, plus a plain-text log with per-subject progress, so you can tell the difference between “still working” and “stalled.”

The script imports cleanly. I’m starting it as a detached Python process now, then I’ll read back the live status file so you have concrete paths to watch while it runs.