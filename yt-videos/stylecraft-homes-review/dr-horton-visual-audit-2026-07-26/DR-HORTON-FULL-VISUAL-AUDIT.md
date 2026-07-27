# Full D.R. Horton Visual Audit

## Finding

Taylor was correct: the affected footage is much more than three or four minutes.

For the current 24 fps CapCut timeline, the conservative replacement/refilm boundary is:

**`00:02:57.042` through `00:25:37.792`**

**Total affected current-timeline runtime: `22:40.750`**

This is one continuous main-track block. It begins with `C6778.MP4` and ends with
`C6787.MP4`. If the goal is to remove every segment filmed in front of, inside, or
as a continuation of the D.R. Horton build—not merely frames where the logo happens
to be legible—replace the entire block.

## Verification basis

- Live CapCut project:
  `/Users/taylordasch_1/Movies/CapCut/User Data/Projects/com.lveditor.draft/0726 (1)`
- Timeline setting: 24 fps
- Timeline ID: `FAF19BF6-9603-498B-85F1-8864EC2426FC`
- Live `draft_info.json` SHA-256:
  `e3c6b10dde3324d2c238ffe5f059a442ee0c2e9a780f9dbc039cf9dbf37a8a26`
- The live project hash matches the transcript/timeline snapshot exactly.
- Every raw clip from `C6778` through `C6787` was sampled every five seconds.
- Start, end, and representative full-resolution frames were also inspected.
- These files are continuous camera takes rather than edited source videos. There
  are no hidden intra-clip hard cuts; the meaningful scene changes occur at the raw
  clip boundaries. The two handheld transition clips, `C6779` and `C6783`, were
  checked from exterior to interior and from interior back toward the exterior.

## Clip-by-clip result

| Raw clip | Raw duration | Current timeline | Used runtime | Visual finding | Disposition |
|---|---:|---|---:|---|---|
| `C6778.MP4` | `05:22.322` | `02:57.042–08:19.375` | `05:22.333` | Exterior A-roll in front of the unfinished house; D.R. Horton branding is readable on the wrap behind Taylor. | Replace all |
| `C6779.MP4` | `00:22.022` | Not used | `00:00.000` | Handheld walk from the branded exterior into the framed house. The wrap explicitly reads “D.R. HORTON America’s Builder.” | Keep out |
| `C6780.MP4` | `00:59.560` | `08:19.375–09:18.958` | `00:59.583` | Interior A-roll inside the same framed structure entered in `C6779`. | Replace all |
| `C6781.MP4` | `06:25.385` | `09:18.958–12:26.125` | `03:07.167` | Interior A-roll in the same structure. Twenty-eight source trims are assembled continuously on the timeline. | Replace all 28 edits |
| `C6782.MP4` | `03:48.729` | `12:26.125–14:44.125` | `02:18.000` | Second interior A-roll angle in the same structure. | Replace all 15 edits |
| `C6783.MP4` | `00:17.017` | Not used | `00:00.000` | Interior B-roll from the same structure; exterior construction wrap is visible again through the opening. | Keep out |
| `C6784.MP4` | `04:38.779` | `14:44.125–18:48.833` | `04:04.708` | Exterior A-roll with large, repeated D.R. Horton branding directly behind Taylor. | Replace all 6 edits |
| `C6785.MP4` | `03:25.706` | `18:48.833–22:14.583` | `03:25.750` | Porch/exterior A-roll; D.R. Horton wrap remains visible at the left and behind Taylor. | Replace all |
| `C6786.MP4` | `02:04.625` | `22:14.583–24:19.208` | `02:04.625` | Exterior A-roll with explicit repeated D.R. Horton wrap. This clip also contains the colored horizontal sensor/exposure band. | Replace all |
| `C6787.MP4` | `01:18.579` | `24:19.208–25:37.792` | `01:18.583` | Same-site exterior continuation immediately after `C6786`, surrounded by the same active construction run. The severe overexposure makes small text unreliable, but the location continuity is clear. | Replace all |
| **Total** | **`28:42.721` raw** | **`02:57.042–25:37.792`** | **`22:40.750`** | **One D.R. Horton-location sequence** | **Replace the full block** |

The raw total is longer because it includes unused takes, discarded source ranges,
and the two unused B-roll clips `C6779` and `C6783`.

## Why the interior footage is included

The readable logo is not visible in every interior crop, but the location does not
change:

1. `C6778` establishes the branded exterior.
2. `C6779` visibly walks through that D.R. Horton-wrapped exterior into the framed
   structure.
3. `C6780`, `C6781`, and `C6782` are the A-roll recorded inside that structure.
4. `C6783` supplies the reverse continuity, showing the same interior and exterior
   wrap through the opening.
5. `C6784` resumes outside with the D.R. Horton wrap plainly visible.

Keeping the interior sections would therefore still present Taylor as reviewing
Stylecraft from inside a D.R. Horton build, even if viewers cannot read a logo in
each individual interior shot.

## Boundary checks

- `C6777`, immediately before the affected block, is a different landscaped/model
  presentation setup and contains no readable D.R. Horton text in the five-second
  audit. Its current timeline segment ends at `02:57.042`.
- `C6778` begins the construction-site sequence at `02:57.042`.
- `C6787` is the final on-camera continuation of that sequence and ends at
  `25:37.792`.
- At `25:37.792`, the main track switches from Taylor’s on-camera A-roll to the DJI
  montage.

This supports `02:57.042–25:37.792` as the clean, conservative replacement span.

## Overlay note

Approximately 43 seconds within the affected block are temporarily covered by
other B-roll overlays:

- `03:09.375–03:23.417`
- `04:42.208–04:51.250`
- `08:15.833–08:21.875`
- `09:45.625–09:51.667`
- `11:49.833–11:57.667`

Those overlays do not reduce the refilm requirement. The underlying spoken
A-roll/audio still comes from the D.R. Horton-site takes, and the current edit
returns to that footage around each overlay.

## Visual evidence

- Five-second contact sheets:
  `contact-sheets-5s/`
- Full-resolution evidence frames:
  `evidence-frames/`
- Boundary-check frames:
  `boundary-checks/`

Contact-sheet indexing is chronological. Each sheet contains up to sixteen
five-second samples. Sheet 1 begins at source `00:00`; sheet 2 begins at source
`01:20`; sheet 3 begins at source `02:40`; and so on.

The clearest single proof frames are:

- `evidence-frames/C6778-060s-house-crop.jpg`
- `evidence-frames/C6779-001s-direct-wrap.jpg`
- `evidence-frames/C6786-120s-full-corrected.jpg`

## Edit instruction

Treat **`02:57.042` as the first frame to replace** and **`25:37.792` as the first
frame after the replacement block**. Re-record the spoken material mapped to
`C6778`, `C6780`, `C6781`, `C6782`, `C6784`, `C6785`, `C6786`, and `C6787`. Do not
reintroduce `C6779` or `C6783` as B-roll.

