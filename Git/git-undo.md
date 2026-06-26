# Git "Oh No" Recipes

When something went wrong — fastest path back. See also [git-cheat-sheet.md](git-cheat-sheet.md).

## Undo the last commit
```bash
git reset --soft HEAD~1        # keep changes staged
git reset --mixed HEAD~1       # keep changes, unstaged
git reset --hard HEAD~1        # nuke the commit AND the changes
```

## Unstage a file (keep edits)
```bash
git restore --staged <file>    # modern
git reset <file>               # old style
```

## Discard local changes to a file
```bash
git restore <file>             # revert file to last commit (destructive)
git checkout -- <file>         # old style
```

## I committed to the wrong branch
```bash
git switch correct-branch
git cherry-pick <commit>       # bring the commit over
git switch wrong-branch
git reset --hard HEAD~1        # remove it from here
```

## I already pushed and need to undo it
```bash
# Safe (shared branch): new commit that reverses it
git revert <commit>
git push

# Rewrite history (only if you're sure no one else pulled):
git reset --hard HEAD~1
git push --force-with-lease    # safer than --force
```

## Recover a deleted branch
```bash
git reflog                     # find the commit the branch pointed to
git switch -c recovered <commit-sha>
```

## Recover a "lost" commit (after a bad reset)
```bash
git reflog                     # find HEAD@{n} before the mistake
git reset --hard HEAD@{n}
```

## Fix the last commit message
```bash
git commit --amend -m "correct message"
# if already pushed:
git push --force-with-lease
```

## Accidentally git add'd a huge/secret file
```bash
git rm --cached <file>         # untrack it, keep on disk
echo "<file>" >> .gitignore
git commit -m "stop tracking <file>"
# If it's a SECRET already pushed: rotate it. History rewrite alone is not enough.
```

## Abort a mid-operation mess
```bash
git merge --abort
git rebase --abort
git cherry-pick --abort
```
