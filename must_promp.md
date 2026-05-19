 make the execution path observable before rerunning anything. That means checking the existing runbook/status
machinery, adding a dedicated detached validation runner with live status files and progress updates if needed, updating the
flowchart to document it, and then launching the validation through that path.
