# Risk And Rollback

## Known Risks

| Risk | Why it matters | Guardrail |
| --- | --- | --- |
| Dirty worktree | Existing modified/deleted files may belong to another workflow. | This project is additive and does not change existing governance, registry, or deleted video files. |
| TikTok lane drift | Older calendars included investor/deal TikTok ideas. | This project follows the current hard rule: TikTok is buyer/relocator native property-tour prep only. |
| GSC partial visibility | Search Console rows are a sample of available performance. | Treat GSC as routing evidence, not the only source of truth. |
| MLS claim misuse | MLS data can include private fields and volatile stats. | Use aggregated public-safe facts with source file/date and caveats. |
| Registry debt | Invalid states and missing page links can make automation noisy. | Repair through a queue before schema changes. |
| Output volume drift | More drafts can lower quality. | Every packet needs lead path, proof notes, and gate check. |

## Rollback

Remove only the files added by this build:

```bash
rm -rf projects/real-estate-social-os-3x
rm scripts/social-os-snapshot.py
```

No existing governance, reference, registry, or content files were intentionally modified by this build.

## Verification Checklist

- `python3 -m py_compile scripts/social-os-snapshot.py`
- `python3 scripts/social-os-snapshot.py --json`
- `python3 scripts/social-os-snapshot.py --out projects/real-estate-social-os-3x/snapshots/latest.md`
- `python3 scripts/output-integrity-check.py --week 2026-W21 --gates`
- Godmode local `score_artifact` on the project docs.
