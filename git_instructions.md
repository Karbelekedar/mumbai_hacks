# Git Workflow Guide for Frontend and Backend Development (Main-only)

## Project Structure
- `frontend/`: NextJS app
- `backend/`: Python server

## Team Structure
- 2 frontend developers
- 2 backend developers

## Branch Structure
- `main`: Stable, production-ready code
- Feature branches: `feature/frontend-<feature-name>`, `feature/backend-<feature-name>`

## Workflow Instructions

### 1. Starting a New Feature

```bash
git checkout main
git pull origin main
git checkout -b feature/frontend-new-feature  # or feature/backend-new-feature
```

### 2. Regular Updates

```bash
git checkout main
git pull origin main
git checkout feature/frontend-new-feature
git rebase main
```

### 3. Completing Frontend Work

```bash
git checkout main
git pull origin main
git merge feature/frontend-new-feature
git push origin main
```

### 4. Starting Backend Work

```bash
git checkout main
git pull origin main
git checkout -b feature/backend-api-update
```

### 5. Completing Backend Work

```bash
git checkout main
git pull origin main
git merge feature/backend-api-update
git push origin main
```

### 6. Integration Testing

Perform integration testing on the `main` branch after each significant merge.

### 7. Pushing Changes to a New Feature Branch

If you're pushing changes from a new feature branch for the first time, you might encounter an error saying "no upstream branch." To resolve this, set the upstream branch by using the following command:

```bash
git push --set-upstream origin <your-feature-branch>
```

## Handling Different Scenarios

### Scenario 1: Your Feature Branch is Behind Main

```bash
git checkout main
git pull origin main
git checkout your-feature-branch
git rebase main
```

### Scenario 2: Your Feature Branch is Ahead of Main

#### Option A: Rebase (Preferred for cleaner history)

```bash
git checkout main
git pull origin main
git checkout your-feature-branch
git rebase main
# If there are conflicts, resolve them
git push origin your-feature-branch --force-with-lease
```

Note: Be cautious with force push. Only do this if you're the only one working on this feature branch.

#### Option B: Merge

```bash
git checkout main
git pull origin main
git merge your-feature-branch
# If there are conflicts, resolve them
git push origin main
```

Choose Option A (rebase) if you want to maintain a linear history and you haven't shared your feature branch with others. Choose Option B (merge) if others are also working on your feature branch or if you want to preserve the exact history of your work.

### Scenario 3: Conflicts During Rebase

```bash
# During rebase, if conflicts occur
git status  # Check which files are in conflict
# Resolve conflicts manually
git add .
git rebase --continue
# If you want to abort the rebase
git rebase --abort
```

### Scenario 4: Emergency Hotfix

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug
# Make changes
git commit -am "Fix critical bug"
git checkout main
git merge hotfix/critical-bug
git push origin main
```

## Best Practices

1. Always pull the latest changes from `main` before starting new work.
2. Commit often with clear, descriptive messages.
3. Use feature branches for all new work.
4. Rebase feature branches on `main` regularly.
5. Perform code reviews before merging into `main`.
6. Run tests locally before pushing to `main`.
7. Communicate with the team before pushing changes to `main`.
8. Consider using pull requests for significant changes, even when merging directly to `main`.
9. Before starting work each day, update your local `main`:
   ```bash
   git checkout main
   git pull origin main
   ```

## Notes

- Replace `feature/frontend-new-feature` and `feature/backend-api-update` with descriptive branch names for your specific features.
- Always ensure you're working on the correct branch before making changes.
- This workflow requires careful coordination. Make sure all team members are aware when changes are being merged to `main`.
- Consider setting up CI/CD to run tests automatically on `main` after each push.
- If you're unsure about any step, don't hesitate to ask for help from your team.

## Workflow for Frontend-Backend Integration

1. Frontend team completes a feature and merges to `main`.
2. Backend team pulls latest `main` and creates a new feature branch for API updates.
3. Backend team implements necessary API changes.
4. Backend team merges API updates to `main`.
5. Frontend team pulls latest `main` and updates their code to use new API endpoints.
6. Both teams test the integration on `main`.
7. If issues are found, create a new feature branch to fix them, then merge back to `main`.

Remember, working directly on `main` requires extra caution. Always communicate with your team before making significant changes, and ensure that `main` remains in a working state at all times.