# Git Worktree Lifecycle: From Creation to Merging

This guide covers the complete workflow of creating a separate Git worktree for a new feature, making changes, and merging those changes back into your `main` branch.

## 1. Creating a Worktree

Assume your main repository is located at `C:\Users\balan\IdeaProjects\my_repo` and you are currently in that directory.

### Scenario A: Creating a NEW branch
If you want to create a brand new branch called `feature_x` and check it out in a new folder:
```powershell
# From the main repo folder
git worktree add -b feature_x ..\my_repo_feature_x_worktree main
```

### Scenario B: Using an EXISTING branch
If the branch `feature_x` already exists and you just want to check it out in a new folder:
```powershell
# From the main repo folder
git worktree add ..\my_repo_feature_x_worktree feature_x
```

## 2. Working in the Worktree

Open the new folder (e.g., `C:\Users\balan\IdeaProjects\my_repo_feature_x_worktree`) in your IDE (like a new VS Code window). 

Make your code changes, stage them, and commit them just like you normally would. The beautiful part about worktrees is that they share the same underlying `.git` history as your main folder.
```powershell
# Inside the worktree folder
git add .
git commit -m "Implement feature X"
```

## 3. Merging the Worktree back to Main

Once your feature is complete and all changes are committed in the worktree, it's time to merge it back into the `main` branch. 

**Important:** You merge *branches*, not folders. Because both folders share the same Git database, you can do this from your main folder.

### Step 3.1: Go back to your main repository folder
You should perform the merge from the folder that has the `main` branch checked out.
```powershell
cd C:\Users\balan\IdeaProjects\my_repo
```

### Step 3.2: Ensure main is up to date
```powershell
git switch main
git pull origin main
```

### Step 3.3: Merge the feature branch
Merge the branch you were working on in your worktree (e.g., `feature_x`) into `main`:
```powershell
git merge feature_x
```
*(Git will automatically bring all the changes you made in the worktree into your main folder.)*

## 4. Cleaning Up

Once the branch is merged successfully, you no longer need the separate worktree folder or the feature branch.

### Step 4.1: Remove the worktree
From your main repository folder, safely remove the worktree folder:
```powershell
git worktree remove ..\my_repo_feature_x_worktree
```
*(If it complains about untracked files you don't care about, you can use `git worktree remove --force ..\my_repo_feature_x_worktree`)*

### Step 4.2: Delete the feature branch
Since the feature is fully merged into `main`, you can cleanly delete the branch:
```powershell
git branch -d feature_x
```
