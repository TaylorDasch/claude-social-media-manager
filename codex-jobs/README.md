# Codex Jobs

Paste-ready prompts for Codex CLI jobs defined in `../CODEX-BACKLOG.md`.

## Launch a job (interactive — recommended)

```bash
cd /Users/taylordasch_1/claude-social-media-manager
git checkout -b codex/<job-slug> main
codex
# then: paste the contents of the corresponding codex-jobs/*.md file
```

## Launch a job (non-interactive)

```bash
cd /Users/taylordasch_1/claude-social-media-manager
git checkout -b codex/<job-slug> main
codex exec "$(cat codex-jobs/cx-01-youtube-metadata.md)"
```

## Parallel worktree (optional — for multiple jobs at once)

```bash
cd /Users/taylordasch_1/claude-social-media-manager
git worktree add ../wt-smm-<job-slug> -b codex/<job-slug> main
cd ../wt-smm-<job-slug>
codex
```

Worktree rollback: `git worktree remove ../wt-smm-<job-slug>` from the SMM repo root.

## Wave 1 launch order

| Card | File | Branch slug |
|------|------|-------------|
| CX-01 | `cx-01-youtube-metadata.md` | `codex/youtube-metadata` |
| CX-02 | `cx-02-keyword-audit.md` | `codex/keyword-audit` |
| CX-04 | `cx-04-performance-ledger.md` | `codex/performance-ledger-auto` |

CX-03 (Postiz) is deferred until Postiz is deployed on Railway.

## After Codex finishes a job

1. Claude (me) reviews the branch diff against the acceptance criteria in `CODEX-BACKLOG.md`.
2. If pass: merge to `main` with a squash commit.
3. If fail: either send Codex back with a correction prompt, or take over manually.
