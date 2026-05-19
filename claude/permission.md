For Claude Code in terminal, the blunt way is:

```bash
claude --dangerously-skip-permissions
```

That disables permission prompts for the session. Anthropic describes it as the bypass-permissions mode, and recommends using it with caution. There is also a newer “auto mode” that reduces prompts more safely, instead of fully disabling them. ([Anthropic][1])

A few important catches:

* It is **session-level**, so you typically start Claude that way each time. ([Anthropic][1])
* Even in bypass mode, writes to some sensitive directories can still prompt, such as `.git`, `.claude`, `.vscode`, and `.idea` (with a few `.claude/*` exceptions). So there is not a true “never ask again for absolutely everything” mode. ([Claude API Docs][2])
* For edits only, Claude Code also has an “Accept all” mode for the current session, but that is not the same as full command permission bypass. ([Claude API Docs][3])

Safer alternative:

```bash
claude --permission-mode auto
```

Anthropic introduced auto mode as a safer middle ground: fewer approval prompts without fully removing safeguards. ([Anthropic][1])

If you want this behavior every time from your shell, add an alias:

```bash
alias claude='claude --dangerously-skip-permissions'
```

Put that in `~/.bashrc` or `~/.zshrc`, then reload your shell:

```bash
source ~/.bashrc
# or
source ~/.zshrc
```

If you want, I can show the exact alias/setup for your shell on macOS, Linux, or Windows PowerShell.

[1]: https://www.anthropic.com/engineering/claude-code-auto-mode?utm_source=chatgpt.com "Claude Code auto mode: a safer way to skip permissions"
[2]: https://docs.anthropic.com/en/docs/claude-code/sub-agents?utm_source=chatgpt.com "Create custom subagents - Claude Code Docs"
[3]: https://docs.anthropic.com/en/docs/claude-code/quickstart?utm_source=chatgpt.com "Quickstart - Claude Code Docs"
