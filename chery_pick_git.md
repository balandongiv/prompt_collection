With a **template repository**, students do **not** get updates automatically after they create their copy. A template gives them a starting snapshot, but GitHub does not keep a built-in upstream link between the new repo and the template repo. ([GitHub Docs][1])

So if the teacher changes something later, students have to bring those changes in **manually**.

The main options are:

**1. Best for future classes: use a fork instead of a template**
If you want students to be able to **sync later updates easily**, a **fork** is better because forks keep a relationship with the original repo and GitHub supports syncing from upstream. GitHub’s docs show fork syncing with the web UI, GitHub CLI, or Git commands. ([GitHub Docs][2])

**2. Keep using template repos, but pull updates manually**
For a repo created from a template, the student can add the teacher repo as another remote and then merge or cherry-pick the new changes. This is a Git workflow, not a GitHub “template sync” feature. Community discussions and marketplace tools exist because template-created repos do not stay linked automatically. ([GitHub][3])

A simple manual method for students is:

```bash
# inside the student's repo
git remote add teacher https://github.com/TEACHER/REPO.git
git fetch teacher
git merge teacher/main
```

If the teacher uses `master` instead of `main`, replace `main` with `master`.

After that:

* Git may merge cleanly, or
* Git may show **conflicts** if the student changed the same lines as the teacher.

Then the student pushes:

```bash
git push origin main
```

Another safer method is to **cherry-pick** only the teacher’s fix commit instead of merging everything:

```bash
git fetch teacher
git log teacher/main
git cherry-pick <commit-hash>
```

That is often better if the teacher only fixed one file or one bug.

My recommendation:

* If this is a **one-time assignment starter**, template repo is fine.
* If the teacher expects to release **fixes after students already start**, use a **fork-based workflow** instead, because GitHub supports syncing forks directly. ([GitHub Docs][2])

You can tell students this:

If the teacher updates the starter code after you already created your repo, your repo will not update automatically.

To get the update:

1. Add the teacher repository as a remote:
   git remote add teacher [https://github.com/TEACHER/REPO.git](https://github.com/TEACHER/REPO.git)

2. Fetch the newest changes:
   git fetch teacher

3. Merge the teacher branch into your branch:
   git merge teacher/main

4. Fix any merge conflicts if Git asks.

5. Push your updated repo:
   git push origin main

If you want, I can turn this into a **teacher workflow** and a **student workflow** with exact commands.

[1]: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository?utm_source=chatgpt.com "Creating a template repository"
[2]: https://docs.github.com/articles/syncing-a-fork?utm_source=chatgpt.com "Syncing a fork"
[3]: https://github.com/orgs/community/discussions/23528?utm_source=chatgpt.com "How to sync repository template changes? #23528"
