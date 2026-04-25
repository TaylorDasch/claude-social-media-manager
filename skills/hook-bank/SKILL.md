# Skill: /hook-bank — Content Hook Generator

## Trigger
"hooks", "hook bank", "need hooks", "hook ideas", "opening lines", "/hook-bank"

## What It Does
Generates 10-15 ready-to-use hooks for a specific content pillar or topic. Hooks are the first 3-7 seconds of a video or the first line of a post — they decide whether someone watches or scrolls. This skill builds a rotating bank so Taylor never sits staring at the camera searching for an opener.

## Input
The user provides ONE of:
1. **A content pillar** — Market Data / Investor Ed / Relocation / Neighborhoods / BTS / Myth-busting
2. **A specific topic** — e.g., "BSW relocation", "Temple TX property taxes", "BRRRR strategy"
3. **"Refill all"** — Generate hooks for every pillar (batch mode)

**Optional:**
- Platform focus: TikTok (3 sec max), YouTube (15 sec max), or Both
- Persona focus: Military / Medical / Investor / Relocator

## Instructions

### Step 1: Load Context
- Read `reference/TEMPLE-TX-DATA-VAULT.md` — pull the freshest, most surprising numbers
- Read `reference/VIDEO-SCRIPT-FORMULAS.md` — hook formulas and proven patterns
- Read `reference/YOUTUBE-GROWTH-PLAYBOOK.md` — retention mechanics, what makes viewers stay
- Read `data/living-in-temple-catalog.txt` and `data/investing-in-temple-catalog.txt` — see what titles already worked (high-performing = good hook)

### Step 2: Check Existing Hook Bank
Read `data/hook-bank.json` (if it exists) to:
- Avoid generating duplicates
- See which hooks were marked "used" so you generate fresh ones
- Check which pillar is running low

### Step 3: Generate Hooks
For the requested pillar/topic, generate 10-15 hooks across these proven formulas:

**Formula 1: The Number Bomb**
Lead with the most surprising specific number.
- "$247K gets you a 3-bed house with a 7.2% cap rate in Temple TX"
- "8,800 employees. One hospital. Zero affordable housing nearby."

**Formula 2: The Myth Killer**
Challenge something everyone assumes is true.
- "Everyone says Temple TX is cheap. Here's what they're not telling you."
- "Buy-and-hold investors are making a huge mistake in 76502 right now."

**Formula 3: The Comparison Trap**
Force a mental comparison the viewer can't ignore.
- "$350K in Austin gets you a condo. In Temple TX it gets you THIS."
- "Killeen's median is $40K less. Here's why it actually costs you MORE."

**Formula 4: The Confession**
Vulnerability that builds instant trust.
- "I almost passed on this deal. Here's why I was wrong."
- "This neighborhood has a problem nobody talks about."

**Formula 5: The Time Bomb**
Create urgency with a deadline or trend.
- "Temple TX inventory just hit 500 homes. Here's what happens next."
- "BSW is hiring 200 more nurses. Here's what that means for rents."

**Formula 6: The Question Nobody Asks**
Reframe the entire conversation.
- "Forget cap rates. There's a better metric for Temple TX investors."
- "The #1 question military families DON'T ask about Fort Hood housing."

**Formula 7: The Insider Drop**
Reveal something only a local would know.
- "Every Temple TX agent knows about 76502. Nobody talks about why."
- "The neighborhood BSW doctors actually live in might surprise you."

### Step 4: Format Each Hook

```markdown
### Hook [#]: [The hook text]
- **Formula:** [which formula above]
- **Platform:** TikTok / YouTube / Both
- **Pillar:** [content pillar]
- **Persona:** [primary target]
- **On-screen text:** [what appears as text overlay — often a shortened version]
- **Visual:** [what the viewer sees — face-to-camera, property, data on screen]
- **Pairs with:** [topic or video idea this hook leads into]
```

### Step 5: Save Output

**Individual request:** Save to `output/YYYY-WXX/hooks/[pillar-or-topic]-hooks.md`

**Also update the master hook bank:** `data/hook-bank.json`
```json
{
  "lastUpdated": "YYYY-MM-DD",
  "hooks": [
    {
      "id": "hook-001",
      "text": "The hook text here",
      "formula": "number-bomb",
      "pillar": "market-data",
      "persona": "investor",
      "platform": "both",
      "pairsWith": "temple-tx-market-update",
      "status": "fresh",
      "dateCreated": "YYYY-MM-DD",
      "dateUsed": null
    }
  ]
}
```

Status values: `fresh` (never used), `used` (Taylor filmed it), `retired` (outdated data or stale)

### Step 6: Batch Mode ("Refill All")
If Taylor says "refill all" or "fill the bank":
1. Check `data/hook-bank.json` for each pillar's count of `fresh` hooks
2. For any pillar with < 5 fresh hooks, generate 10 new ones
3. Retire any hooks with data older than 60 days (prices, inventory counts change)
4. Output a summary: "Generated X new hooks. Bank now has Y fresh hooks across Z pillars."

## Rules
- Every hook MUST contain a specific number, neighborhood name, or verifiable claim. No generic hooks.
- Hooks must be TRUE — don't exaggerate data for shock value. The real numbers are shocking enough.
- No banned words: turnkey, dream home, charming, nestled, white glove, Fort Cavazos
- "Fort Hood" not "Fort Cavazos" (name reverted July 2025)
- "Buy-and-hold" not "turnkey"
- TikTok hooks: 3 seconds spoken max. The text overlay carries the data. Face + energy first.
- YouTube hooks: Up to 15 seconds. Can include a brief visual (property shot, data screenshot) before face-to-camera.
- Never repeat a hook from the existing bank. Always check first.
- Data in hooks should come from `reference/TEMPLE-TX-DATA-VAULT.md`. If the data vault is stale, flag it: "DATA VAULT NEEDS REFRESH: [specific number] may be outdated."
- The "Pairs with" field matters — every hook should lead somewhere. A great hook with no video behind it is wasted.

## Dependencies
- Reads `reference/TEMPLE-TX-DATA-VAULT.md`, `reference/VIDEO-SCRIPT-FORMULAS.md`, `reference/YOUTUBE-GROWTH-PLAYBOOK.md`
- Reads `data/living-in-temple-catalog.txt`, `data/investing-in-temple-catalog.txt`
- Reads/writes `data/hook-bank.json` (master bank)
- Saves weekly output to `output/YYYY-WXX/hooks/`
