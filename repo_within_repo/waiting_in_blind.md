You’re right. The last validation command was running in the background terminal, which gives you no usable visibility from your side. I’m checking whether anything is still
running now, and then I’ll switch to the visible Experiment 1A launcher path so you can watch progress in a separate PowerShell window instead of waiting blind.

The observable runner is live, but the durable status files still only show stage start because Stage 4 itself doesn’t emit intermediate heartbeat updates yet. I’m checking the
launcher-side log directory and the active process state next so I can tell you whether it’s genuinely computing or stuck at startup.

One limitation remains: status.md only updates when a stage finishes, not during the middle of Stage 4. So for live movement during analyze, the detached PowerShell window is the
real-time view. I’m checking the active process CPU once so I can confirm it’s actually working rather than idling.