You already launched OpenAI Codex once (that banner proves it), but now your shell says `codex: command not found`, which usually means one of these:

1. It was launched from another shell/session
2. It was installed via `npx` and not globally available
3. PATH changed after activating `.venv`

### Quick check

Run:

```bash
which codex
```

and

```bash
npm list -g --depth=0 | grep codex
```

### Most common fix: run with npx

Try:

```bash
npx @openai/codex --dangerously-bypass-approvals-and-sandbox
```

This works even if it is not globally installed.

### If you want it globally available

Install globally:

```bash
npm install -g @openai/codex
```

then:

```bash
codex --dangerously-bypass-approvals-and-sandbox
```

### If npm is missing

Check:

```bash
node -v
npm -v
```

If missing, install Node.js first.

### About the bubblewrap warning

That warning is not the reason for `command not found`. It just means Linux sandboxing dependency `bubblewrap` is missing.

On Ubuntu/Debian:

```bash
sudo apt install bubblewrap
```

But your immediate issue is that `codex` itself is not on PATH.
