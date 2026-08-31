# Automation Data Sources

This branch is a narrow data bridge for cloud routines. It intentionally carries only the current content registry and performance ledger needed by reporting jobs.

- `data/content-registry.csv` is sourced from the active `claude-social-media-manager` workspace.
- `data/performance-ledger.csv` is sourced from the active clean-main worktree.
- Cloud jobs must check file timestamps and dates before making recommendations.
- Missing or stale data must be reported as unavailable; jobs must not fall back to Follow Up Boss, hard-coded deal lists, or historical snapshots.

The branch is maintained independently so large media assets and unrelated working-tree changes never enter the automation data path.
