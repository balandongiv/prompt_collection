Yes — what IntelliJ is effectively doing is **auto-stash + rebase + re-apply your local changes**.

In VS Code, the built-in Git UI is usually stricter and may block **Pull (Rebase)** when your working tree is dirty. Git itself can do the IntelliJ-style behavior though, by enabling **autostash** for rebase. Git’s rebase supports `--autostash`, and the related config is `rebase.autoStash`; `git pull --rebase` is the pull mode that uses rebase. ([Git SCM][1])

Run this once:

```bash
git config --global pull.rebase true
git config --global rebase.autoStash true
```

Then from terminal in VS Code, a normal pull will behave much closer to IntelliJ:

```bash
git pull
```

Or explicitly:

```bash
git pull --rebase --autostash
```

What this does:

* temporarily stashes your uncommitted changes,
* pulls and rebases,
* then reapplies your changes afterward. ([Git SCM][1])

A few important notes:

* **VS Code’s button/menu may still complain** even if Git is configured this way, because the UI can enforce a clean-tree check before invoking the operation.
* In that case, use the **integrated terminal** in VS Code instead of the menu action.
* If your local edits overlap with incoming changes, the final re-apply can still produce conflicts. Git’s docs explicitly warn about that. ([Git SCM][1])

If you want a VS Code workflow that feels closest to IntelliJ, use one of these:

1. **Terminal-first:** `git pull --rebase --autostash`
2. **Manual stash in UI:** stash → pull rebase → pop stash
3. **Worktrees** for cleaner branch switching; VS Code supports Git stashes and worktrees, but for local repos it does not promise the same “switch freely with dirty changes” behavior that the GitHub Repositories extension has for remote repos. ([Visual Studio Code][2])

To check whether your config is active:

```bash
git config --global --get pull.rebase
git config --global --get rebase.autoStash
```

If you want, I can also show how to make a **VS Code task or alias** so one shortcut does IntelliJ-style pull/rebase automatically.

[1]: https://git-scm.com/docs/git-rebase?utm_source=chatgpt.com "Git - git-rebase Documentation"
[2]: https://code.visualstudio.com/docs/sourcecontrol/branches-worktrees?utm_source=chatgpt.com "Git Branches and Worktrees in VS Code"
