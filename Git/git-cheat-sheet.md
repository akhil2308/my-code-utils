# Git Cheat Sheet

Daily commands I actually reach for. See also [git rebase.md](git%20rebase.md) and [git-undo.md](git-undo.md).

## Status & inspect
```bash
git status -sb                 # short status + branch
git log --oneline --graph --all -20
git diff                       # unstaged changes
git diff --staged              # staged changes
git show <commit>              # what a commit changed
git blame <file>               # who last touched each line
```

## Branching
```bash
git switch -c feature/x        # create + switch (modern)
git switch main                # switch back
git branch -d feature/x        # delete merged branch
git branch -D feature/x        # force delete
git branch -m old new          # rename current/other branch
```

## Stash
```bash
git stash                      # shelve tracked changes
git stash -u                   # include untracked
git stash list
git stash pop                  # apply + drop latest
git stash apply stash@{2}      # apply specific, keep it
git stash drop stash@{0}
```

## Commit
```bash
git commit -m "msg"
git commit --amend             # edit last commit (message or staged content)
git commit --amend --no-edit   # add staged files to last commit, keep message
```

## Cherry-pick
```bash
git cherry-pick <commit>       # apply one commit here
git cherry-pick A^..B          # range (A exclusive) .. B
git cherry-pick --continue     # after resolving conflicts
git cherry-pick --abort
```

## Reset vs revert
```bash
git reset --soft HEAD~1        # undo commit, KEEP changes staged
git reset --mixed HEAD~1       # undo commit, keep changes unstaged (default)
git reset --hard HEAD~1        # undo commit, DISCARD changes (destructive)
git revert <commit>            # new commit that undoes <commit> (safe on shared history)
```

## Clean untracked
```bash
git clean -n                   # dry run — show what would be deleted
git clean -fd                  # delete untracked files + dirs
```

## Reflog — the safety net
```bash
git reflog                     # every HEAD move, even "lost" commits
git reset --hard HEAD@{3}      # jump back to a prior state
```

## Bisect — find the bad commit
```bash
git bisect start
git bisect bad                 # current is broken
git bisect good <commit>       # known-good commit
# git checks out a midpoint — test, then mark:
git bisect good   # or: git bisect bad
git bisect reset               # done
```

## Remotes & tags
```bash
git remote -v
git fetch --all --prune        # update remotes, drop deleted branches
git push -u origin HEAD        # push current branch + set upstream
git tag -a v1.0 -m "release"   # annotated tag
git push origin --tags
```
