Use this from the **main repo** or any other worktree:

```bash
git worktree remove <path-to-worktree>
```

Example:

```bash
git worktree remove C:\Users\balan\IdeaProjects\ear_eog_experiment_feature_branch
```

Git’s `worktree remove` deletes the linked worktree, but only if it is **clean**. If there are modified or untracked files, or it has submodules, you need `--force`. The **main worktree cannot be removed** with this command. ([Git SCM][1])

So if Git refuses, use:

```bash
git worktree remove --force C:\Users\balan\IdeaProjects\ear_eog_experiment_feature_branch
```

A good safe workflow is:

```bash
git worktree list
git worktree remove C:\path\to\worktree
```

If you already deleted the folder manually in File Explorer, clean up stale metadata with:

```bash
git worktree prune
```

Git’s docs note that if a linked worktree is deleted manually, its admin files are eventually cleaned automatically, or you can run `git worktree prune` yourself. ([Git SCM][2])

If you also want to delete the branch associated with that worktree afterward, run:

```bash
git branch -d <branch-name>
```

or force it:

```bash
git branch -D <branch-name>
```

[1]: https://git-scm.com/docs/git-worktree?utm_source=chatgpt.com "Git - git-worktree Documentation"
[2]: https://git-scm.com/docs/git-worktree/2.28.0?utm_source=chatgpt.com "Git - git-worktree Documentation"
