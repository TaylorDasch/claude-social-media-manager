# Candidates Index

## Round 1 candidates

| Label | Author | File |
|---|---|---|
| A | Cold-start author, task only | `r1-candidate-A.md` |
| B | Author-B with task + A + critique | `r1-candidate-B.md` |
| AB | Synthesizer with task + A + B | `r1-candidate-AB.md` |

## Round 1 critic + judges

| File | Description |
|---|---|
| `r1-critic.md` | Adversarial attack on Candidate A — 12 weaknesses (2 FATAL, 7 MAJOR, 3 MINOR) |
| `r1-judge-transcripts.md` | Full 5-judge transcripts with decoded labels (X=AB, Y=A, Z=B) |

## Round 2 candidates

| Label | Author | File |
|---|---|---|
| A' | Cold-start author, incumbent = AB | `r2-candidate-A.md` |
| B' | Author-B with task + A' + critique | `r2-candidate-B.md` |
| AB' | Synthesizer with task + A' + B' | `r2-candidate-AB.md` |

## Round 2 critic + judges

| File | Description |
|---|---|
| `r2-critic.md` | Adversarial attack on Candidate A' — 8 weaknesses (0 FATAL, 4 MAJOR, 4 MINOR) |
| `r2-judge-transcripts.md` | Full 5-judge transcripts with decoded labels (X=B', Y=AB', Z=A') |

## Final ship candidate

**AB'** — extracted and split into production files in parent folder:
- `../script.md`
- `../titles-thumbnails.md`
- `../description-pinned.md`
- `../shot-list.md`
- `../shorts.md`

## Companion lineage files

| File | Description |
|---|---|
| `overview.md` | Executive summary of the council run |
| `lineage.md` | Human-readable round-by-round trace |
| `reason-results.tsv` | Per-round log: round, winner, votes, consecutive_wins, word_counts |
| `reason-lineage.jsonl` | Machine-readable full lineage |
| `handoff.json` | Chain handoff schema |
