"""
Taylor Dasch Social Media Manager — Telegram Bot
Powered by Claude Sonnet via Anthropic API

Features:
  - Content generation commands (TikTok, YouTube, GMB, etc.)
  - Weekly production scorecard with YouTube auto-scanning
  - Manual /done tracking for non-YouTube content
  - Scheduled autopilot (daily GMB, Monday calendar, Tuesday filming, Friday scorecard)
"""

import os
import json
import logging
from datetime import time, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import anthropic
from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ChatAction, ParseMode

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]
AUTHORIZED_USER_ID = os.environ.get("AUTHORIZED_USER_ID")  # optional lock-down
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")  # optional — enables auto-scanning
MODEL = "claude-sonnet-4-6"
TIMEZONE = ZoneInfo("America/Chicago")

# YouTube channel IDs
YT_CHANNEL_LIVING = os.environ.get("YT_CHANNEL_LIVING", "UCqrLPGPR9eV7QUfK02dwtpQ")
YT_CHANNEL_INVESTING = os.environ.get("YT_CHANNEL_INVESTING", "")  # Add when known

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Load config
# ---------------------------------------------------------------------------
CONFIG_PATH = Path(__file__).resolve().parent.parent / "social-media-config.json"
STATE_PATH = Path(__file__).resolve().parent / "scorecard_state.json"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


CONFIG = load_config()


# ---------------------------------------------------------------------------
# Weekly Production Tracker
# ---------------------------------------------------------------------------
WEEKLY_TARGETS = {
    "yt_longform": {"target": 1, "label": "YouTube Long-form", "emoji": "YT"},
    "yt_shorts": {"target": 2, "label": "YouTube Shorts", "emoji": "YTS"},
    "tiktok": {"target": 3, "label": "TikTok Posts", "emoji": "TT"},
    "gmb": {"target": 5, "label": "GMB Posts", "emoji": "GMB"},
    "community": {"target": 2, "label": "Community Posts", "emoji": "CP"},
    "blog": {"target": 1, "label": "Blog Posts", "emoji": "BG"},
    "newsletter": {"target": 1, "label": "Newsletter", "emoji": "NL"},
    "forum": {"target": 2, "label": "BP/Reddit Replies", "emoji": "FR"},
    "dotw": {"target": 1, "label": "Deal of the Week", "emoji": "DW"},
    "audit": {"target": 1, "label": "AEO Audit", "emoji": "AU"},
    "linkedin": {"target": 0, "label": "LinkedIn Carousel", "emoji": "LI"},
}


def get_iso_week() -> str:
    """Get current ISO week as YYYY-WXX."""
    now = datetime.now(TIMEZONE)
    return f"{now.isocalendar()[0]}-W{now.isocalendar()[1]:02d}"


def get_week_date_range() -> str:
    """Get Monday-Sunday date range for current week."""
    now = datetime.now(TIMEZONE)
    monday = now - timedelta(days=now.weekday())
    sunday = monday + timedelta(days=6)
    return f"{monday.strftime('%b %d')} - {sunday.strftime('%b %d')}"


def load_state() -> dict:
    """Load persistent scorecard state."""
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(state: dict):
    """Save scorecard state to disk."""
    try:
        with open(STATE_PATH, "w") as f:
            json.dump(state, f, indent=2)
    except OSError as e:
        logger.error(f"Failed to save state: {e}")


def get_week_state() -> dict:
    """Get or create state for the current week."""
    state = load_state()
    week = get_iso_week()

    if state.get("week") != week:
        # New week — reset tracker, archive previous
        prev = state.get("week")
        prev_counts = state.get("counts", {})
        state = {
            "week": week,
            "counts": {k: 0 for k in WEEKLY_TARGETS},
            "items": [],  # Log of what was done
            "yt_scanned": [],  # Video IDs already counted
            "previous_week": prev,
            "previous_counts": prev_counts,
        }
        save_state(state)

    # Ensure all keys exist (in case targets were added after state was created)
    for k in WEEKLY_TARGETS:
        if k not in state.get("counts", {}):
            state.setdefault("counts", {})[k] = 0

    return state


def update_count(category: str, amount: int = 1, description: str = "") -> str:
    """Increment a category count and log the item."""
    state = get_week_state()
    if category not in WEEKLY_TARGETS:
        return f"Unknown category: {category}"

    state["counts"][category] = state["counts"].get(category, 0) + amount
    if description:
        state["items"].append({
            "category": category,
            "description": description,
            "timestamp": datetime.now(TIMEZONE).isoformat(),
        })
    save_state(state)

    current = state["counts"][category]
    target = WEEKLY_TARGETS[category]["target"]
    label = WEEKLY_TARGETS[category]["label"]
    return f"{label}: {current}/{target} {'done' if current >= target else ''}"


# ---------------------------------------------------------------------------
# YouTube API Scanner
# ---------------------------------------------------------------------------
def scan_youtube_uploads() -> dict:
    """Scan YouTube channels for this week's uploads. Returns counts and video list."""
    if not YOUTUBE_API_KEY:
        return {"available": False, "reason": "No YOUTUBE_API_KEY configured"}

    try:
        from googleapiclient.discovery import build
    except ImportError:
        return {"available": False, "reason": "google-api-python-client not installed"}

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Calculate start of current week (Monday 00:00 CT)
    now = datetime.now(TIMEZONE)
    monday = now - timedelta(days=now.weekday())
    week_start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    published_after = week_start.isoformat()

    results = {
        "available": True,
        "longform": [],
        "shorts": [],
        "total_views": 0,
    }

    channels = [
        ("Living in Temple", YT_CHANNEL_LIVING),
        ("Investing in Temple", YT_CHANNEL_INVESTING),
    ]

    for channel_name, channel_id in channels:
        if not channel_id:
            continue

        try:
            # Search for videos published this week
            search = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                publishedAfter=published_after,
                type="video",
                order="date",
                maxResults=20,
            ).execute()

            video_ids = [item["id"]["videoId"] for item in search.get("items", [])]
            if not video_ids:
                continue

            # Get video details (duration, stats)
            details = youtube.videos().list(
                part="contentDetails,statistics,snippet",
                id=",".join(video_ids),
            ).execute()

            for video in details.get("items", []):
                duration = video["contentDetails"]["duration"]  # e.g., PT14M54S or PT44S
                title = video["snippet"]["title"]
                video_id = video["id"]
                views = int(video.get("statistics", {}).get("viewCount", 0))
                likes = int(video.get("statistics", {}).get("likeCount", 0))
                published = video["snippet"]["publishedAt"]

                results["total_views"] += views

                video_info = {
                    "id": video_id,
                    "title": title,
                    "channel": channel_name,
                    "duration": duration,
                    "views": views,
                    "likes": likes,
                    "published": published,
                }

                # Parse duration to classify as short vs longform
                # Shorts are typically < 3 minutes
                is_short = _duration_seconds(duration) < 180
                if is_short:
                    results["shorts"].append(video_info)
                else:
                    results["longform"].append(video_info)

        except Exception as e:
            logger.error(f"YouTube API error for {channel_name}: {e}")

    return results


def _duration_seconds(iso_duration: str) -> int:
    """Parse ISO 8601 duration (PT14M54S) to seconds."""
    import re
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def sync_youtube_to_state():
    """Pull YouTube uploads and update scorecard state (deduped by video ID)."""
    yt_data = scan_youtube_uploads()
    if not yt_data.get("available"):
        return yt_data

    state = get_week_state()
    scanned = set(state.get("yt_scanned", []))
    new_longform = 0
    new_shorts = 0

    for video in yt_data["longform"]:
        if video["id"] not in scanned:
            scanned.add(video["id"])
            new_longform += 1
            state["items"].append({
                "category": "yt_longform",
                "description": f"{video['title']} ({video['channel']})",
                "timestamp": video["published"],
                "auto": True,
            })

    for video in yt_data["shorts"]:
        if video["id"] not in scanned:
            scanned.add(video["id"])
            new_shorts += 1
            state["items"].append({
                "category": "yt_shorts",
                "description": f"{video['title']} ({video['channel']})",
                "timestamp": video["published"],
                "auto": True,
            })

    state["counts"]["yt_longform"] = state["counts"].get("yt_longform", 0) + new_longform
    state["counts"]["yt_shorts"] = state["counts"].get("yt_shorts", 0) + new_shorts
    state["yt_scanned"] = list(scanned)
    save_state(state)

    return {
        **yt_data,
        "new_longform": new_longform,
        "new_shorts": new_shorts,
    }


# ---------------------------------------------------------------------------
# Scorecard Formatter
# ---------------------------------------------------------------------------
def format_scorecard(include_yt_scan: bool = True) -> str:
    """Generate the formatted scorecard message."""
    state = get_week_state()

    # Optionally sync YouTube first
    yt_status = ""
    if include_yt_scan:
        yt_data = sync_youtube_to_state()
        state = get_week_state()  # Reload after sync
        if yt_data.get("available"):
            yt_status = f"\nYouTube auto-scan: {len(yt_data.get('longform', []))} long-form, {len(yt_data.get('shorts', []))} shorts detected"
            if yt_data.get("total_views", 0) > 0:
                yt_status += f" ({yt_data['total_views']:,} views this week)"
        else:
            yt_status = f"\nYouTube scan: {yt_data.get('reason', 'unavailable')}"

    counts = state.get("counts", {})
    week = state.get("week", get_iso_week())
    date_range = get_week_date_range()

    # Calculate score
    targets_hit = 0
    total_targets = 0
    for key, info in WEEKLY_TARGETS.items():
        if info["target"] > 0:
            total_targets += 1
            if counts.get(key, 0) >= info["target"]:
                targets_hit += 1

    # Build the scorecard
    lines = [
        f"*Weekly Scorecard: {week}*",
        f"_{date_range}_",
        f"",
        f"*Score: {targets_hit}/{total_targets} targets hit*",
        f"",
    ]

    for key, info in WEEKLY_TARGETS.items():
        current = counts.get(key, 0)
        target = info["target"]
        label = info["label"]

        if target == 0:
            # Optional item
            if current > 0:
                lines.append(f"  {label}: {current} (bonus)")
            continue

        if current >= target:
            bar = "done"
        elif current > 0:
            bar = f"{current}/{target}"
        else:
            bar = f"0/{target} -- MISSING"

        lines.append(f"  {label}: {bar}")

    # Show what was logged
    items = state.get("items", [])
    if items:
        lines.append("")
        lines.append("*Activity Log:*")
        # Show last 10 items
        for item in items[-10:]:
            auto_tag = " (auto)" if item.get("auto") else ""
            ts = item.get("timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts)
                    ts = dt.strftime("%a %I:%M%p")
                except (ValueError, TypeError):
                    ts = ""
            desc = item.get("description", item.get("category", ""))
            lines.append(f"  {ts} — {desc}{auto_tag}")

    if yt_status:
        lines.append(yt_status)

    # Gaps analysis
    gaps = []
    for key, info in WEEKLY_TARGETS.items():
        if info["target"] > 0 and counts.get(key, 0) < info["target"]:
            remaining = info["target"] - counts.get(key, 0)
            gaps.append(f"{info['label']} ({remaining} remaining)")

    if gaps:
        lines.append("")
        lines.append("*Gaps to close:*")
        for g in gaps:
            lines.append(f"  - {g}")

    # Compare to previous week if available
    prev = state.get("previous_counts", {})
    if prev:
        prev_hits = 0
        for key, info in WEEKLY_TARGETS.items():
            if info["target"] > 0 and prev.get(key, 0) >= info["target"]:
                prev_hits += 1
        trend = targets_hit - prev_hits
        if trend > 0:
            lines.append(f"\n_Trend: +{trend} vs last week_")
        elif trend < 0:
            lines.append(f"\n_Trend: {trend} vs last week_")
        else:
            lines.append(f"\n_Trend: same as last week_")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Parse /done input
# ---------------------------------------------------------------------------
DONE_ALIASES = {
    # YouTube
    "yt": "yt_longform", "youtube": "yt_longform", "video": "yt_longform",
    "long": "yt_longform", "longform": "yt_longform", "filmed": "yt_longform",
    # Shorts
    "short": "yt_shorts", "shorts": "yt_shorts", "reel": "yt_shorts", "reels": "yt_shorts",
    # TikTok
    "tiktok": "tiktok", "tt": "tiktok", "tiktoks": "tiktok", "tok": "tiktok",
    # GMB
    "gmb": "gmb", "google": "gmb",
    # Community
    "community": "community", "cp": "community",
    # Blog
    "blog": "blog", "post": "blog", "article": "blog",
    # Newsletter
    "newsletter": "newsletter", "nl": "newsletter", "email": "newsletter",
    # Forum
    "forum": "forum", "bp": "forum", "reddit": "forum", "biggerpockets": "forum", "reply": "forum",
    # Deal of the Week
    "dotw": "dotw", "deal": "dotw",
    # Audit
    "audit": "audit", "aeo": "audit",
    # LinkedIn
    "linkedin": "linkedin", "li": "linkedin", "carousel": "linkedin",
}


def parse_done_input(text: str) -> tuple[str | None, int, str]:
    """
    Parse done input like:
      'gmb' -> (gmb, 1, '')
      '3 tiktoks' -> (tiktok, 3, '')
      'filmed canyon creek video' -> (yt_longform, 1, 'canyon creek video')
      'bp reply about taxes' -> (forum, 1, 'reply about taxes')
    Returns: (category, count, description)
    """
    text = text.strip().lower()
    words = text.split()

    if not words:
        return None, 0, ""

    # Check for leading number: "3 tiktoks"
    count = 1
    if words[0].isdigit():
        count = int(words[0])
        words = words[1:]

    if not words:
        return None, count, ""

    # Try matching first word(s) to aliases
    for i in range(min(2, len(words)), 0, -1):
        key = " ".join(words[:i])
        # Try exact alias match
        if key in DONE_ALIASES:
            category = DONE_ALIASES[key]
            description = " ".join(words[i:])
            return category, count, description

        # Try partial match on alias keys
        for alias, cat in DONE_ALIASES.items():
            if alias.startswith(key) or key.startswith(alias):
                description = " ".join(words[i:]) if i < len(words) else ""
                return cat, count, description

    # Try matching against full text for keywords anywhere
    for alias, cat in DONE_ALIASES.items():
        if alias in words:
            idx = words.index(alias)
            remaining = [w for j, w in enumerate(words) if j != idx]
            return cat, count, " ".join(remaining)

    return None, count, text


# ---------------------------------------------------------------------------
# Anthropic client
# ---------------------------------------------------------------------------
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# Simple per-chat conversation buffer (last 6 messages for context)
chat_history: dict[int, list[dict]] = {}
MAX_HISTORY = 6

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = f"""You are Taylor Dasch's Social Media Manager bot. You generate ready-to-use content for his real estate brand.

TODAY'S DATE: {datetime.now(TIMEZONE).strftime('%A, %B %d, %Y')}

CRITICAL RULES:
- Voice: Analytical, data-driven, honest. Taylor speaks like an investor-analyst, NOT a salesperson.
- NEVER say "turnkey" — always "buy-and-hold investors"
- "Scars and All" rule: Include honest negatives when real.
- Question Hook → Answer First on all content.
- 7-Second Pattern Interrupt rule for video scripts.
- Comments never fully answer — push to DM for expanded value.
- Key stats: $27M+ volume, 100+ transactions, 3yr BP Featured Agent, 76502 Power Zip (753/1000 score, 5,101 unit deficit, 24.1% growth)
- BSW: 8,800+ employees. BAH E-6 w/dep: $1,920/mo tax-free. PGY-1 stipend: $70,993/yr.
- Temple median home: $247,450-$288,000. Active inventory: 500+. DOM: 83 days.
- Brand colors: Midnight #1e293b, Emerald #059669, Snow #f8fafc
- Slogan: "Build | Serve | Grow"

TIKTOK RULES:
- 5 pillars: Property Tours, Relocation/Military/Medical, Market Data/Investor, Only in Texas/Lifestyle, BTS
- Never 2 of same pillar in a row
- 5-10 hashtags per post (3-tier: 1-2 broad, 2-3 niche, 3-4 local)
- DM keyword triggers: GUIDE, DEALS, TOUR, BAH, BSW, RELOCATE, TEMPLE
- Video length: 21-34 sec (promoted), 30-60 sec (talking head), 15-60 sec (tours)
- Posting windows: Mon 12:30, Tue-Wed 8:30-10:30, Thu-Fri 3:30-5:30, Sat 8:30-12:30, Sun 8:30

YOUTUBE RULES:
- Two channels: "Living in Temple" (relocation) + "Investing in Temple" (investor)
- Entity declaration first 10 sec: "Hi, I'm Taylor Dasch with EG Realty..."
- Deal of the Week every Tuesday on Investing channel
- Description: 7-section template (answer, context, timestamps, areas, data, about, contact)

GMB POSTS:
- Bible verse + Business Acumen Micro-Lesson
- Include newsletter link
- Rotate themes: Mon=work ethic, Tue=service, Wed=wisdom, Thu=perseverance, Fri=community, Sat=stewardship, Sun=faith

NEWSLETTER:
- 3 sections: The Deep Dive (~400 words), The Deal Autopsy (real numbers + scars), Bell County Bulletin (3-5 bullets)
- Subject line formulas: [Data Point] + What It Means / The Question / The Honest Contrary Take / The Surprising Number / The Local Intel Play

REDDIT (Month 1 — pure value, no links):
- Target subs: r/realestateinvesting, r/militaryfinance, r/landlord, r/personalfinance, r/Texas
- Reply framework: Validate (1-2 sentences) → Meat (200-400 words, hyperlocal data) → Soft close

PERSONAS:
1. Military Relocator (Fort Hood) — PCS, BAH, VA loans
2. BSW Medical Professional — commute zones, physician loans, residency cycle
3. Out-of-State Buy-and-Hold Investor — cap rates, DSCR, macro catalysts
4. Luxury Buyer ($600K-$1.2M) — appreciation play, acreage, Belton ISD

FORMAT YOUR RESPONSES for Telegram (use markdown sparingly — bold with *text*, code with `text`). Keep responses actionable and ready to copy-paste. For long content, use clear section headers.

FULL CONFIG DATA:
{json.dumps(CONFIG, indent=2)[:8000]}
"""


def get_system_prompt() -> str:
    """Return system prompt with today's date refreshed."""
    today = datetime.now(TIMEZONE).strftime("%A, %B %d, %Y")
    return SYSTEM_PROMPT.replace(
        SYSTEM_PROMPT.split("TODAY'S DATE: ")[1].split("\n")[0],
        today,
    )


# ---------------------------------------------------------------------------
# Auth check
# ---------------------------------------------------------------------------
def is_authorized(update: Update) -> bool:
    if not AUTHORIZED_USER_ID:
        return True  # no lock-down configured
    return str(update.effective_user.id) == AUTHORIZED_USER_ID


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def split_message(text: str, max_len: int = 4096) -> list[str]:
    """Split long text into Telegram-safe chunks."""
    if len(text) <= max_len:
        return [text]
    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        # Try to split at a newline
        idx = text.rfind("\n", 0, max_len)
        if idx == -1:
            idx = max_len
        chunks.append(text[:idx])
        text = text[idx:].lstrip("\n")
    return chunks


async def ask_claude(chat_id: int, user_message: str) -> str:
    """Send message to Claude with conversation context and return response."""
    history = chat_history.get(chat_id, [])
    history.append({"role": "user", "content": user_message})

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=get_system_prompt(),
            messages=history[-MAX_HISTORY:],
        )
        assistant_text = response.content[0].text

        # Update history
        history.append({"role": "assistant", "content": assistant_text})
        chat_history[chat_id] = history[-MAX_HISTORY:]

        return assistant_text
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return f"API error: {e}"


async def send_response(update: Update, text: str):
    """Send a potentially long response, split into chunks."""
    for chunk in split_message(text):
        try:
            await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            # Fall back to plain text if markdown parsing fails
            await update.message.reply_text(chunk)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Not authorized.")
        return

    user_id = update.effective_user.id
    welcome = (
        f"*Taylor Dasch Social Media Manager*\n\n"
        f"Your Telegram user ID: `{user_id}`\n\n"
        f"*Content Commands:*\n"
        f"/tiktok [topic] — TikTok script\n"
        f"/calendar — This week's content calendar\n"
        f"/gmb — Today's GMB post\n"
        f"/dotw [details] — Deal of the Week package\n"
        f"/youtube [topic] — YouTube description\n"
        f"/newsletter [topic] — Newsletter draft\n"
        f"/hooks [pillar] — Generate new hooks\n"
        f"/reddit [topic] — Reddit reply draft\n"
        f"/bp [topic] — BiggerPockets reply draft\n"
        f"/repurpose — Repurpose last content\n\n"
        f"*Scorecard Commands:*\n"
        f"/scorecard — View this week's production score\n"
        f"/done [item] — Mark something as done\n"
        f"/undo [item] — Remove one from a category\n\n"
        f"*Done examples:*\n"
        f"`/done gmb` — logged 1 GMB post\n"
        f"`/done 3 tiktoks` — logged 3 TikToks\n"
        f"`/done filmed canyon creek video` — logged 1 YT video\n"
        f"`/done bp reply about taxes` — logged 1 forum reply\n"
        f"`/done blog BSW commute guide` — logged 1 blog post\n"
        f"`/done newsletter` — logged newsletter\n\n"
        f"*Autopilot active:*\n"
        f"- Daily 6:00 AM CT: GMB post\n"
        f"- Monday 6:00 AM CT: Weekly content calendar\n"
        f"- Tuesday 6:00 AM CT: Filming day scripts\n"
        f"- Friday 5:00 PM CT: Weekly scorecard"
    )
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)


async def cmd_scorecard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the current week's production scorecard."""
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    scorecard = format_scorecard(include_yt_scan=True)
    await send_response(update, scorecard)


async def cmd_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mark something as done on the scorecard."""
    if not is_authorized(update):
        return

    text = " ".join(context.args) if context.args else ""
    if not text:
        categories = "\n".join(
            f"  `{k}` — {v['label']} (target: {v['target']}/wk)"
            for k, v in WEEKLY_TARGETS.items()
            if v["target"] > 0
        )
        await update.message.reply_text(
            f"*What did you do?*\n\n"
            f"Examples:\n"
            f"`/done gmb`\n"
            f"`/done 3 tiktoks`\n"
            f"`/done filmed BSW video`\n"
            f"`/done bp reply about cap rates`\n"
            f"`/done blog` or `/done newsletter`\n\n"
            f"*Categories:*\n{categories}",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    category, count, description = parse_done_input(text)

    if not category:
        # Couldn't parse — ask Claude to help interpret
        await update.message.chat.send_action(ChatAction.TYPING)
        prompt = (
            f"Taylor said he completed: '{text}'\n\n"
            f"Map this to one of these content categories and respond with ONLY the category key:\n"
            f"{json.dumps({k: v['label'] for k, v in WEEKLY_TARGETS.items()})}\n\n"
            f"If unclear, respond with 'UNCLEAR' and ask what they mean."
        )
        response = await ask_claude(update.message.chat_id, prompt)
        response_clean = response.strip().lower().replace("'", "").replace('"', '')

        if response_clean in WEEKLY_TARGETS:
            category = response_clean
        else:
            await update.message.reply_text(
                f"Couldn't figure out the category. Try:\n"
                f"`/done gmb`, `/done tiktok`, `/done blog`, `/done video`, etc.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

    result = update_count(category, count, description or text)
    await update.message.reply_text(f"Logged! {result}")


async def cmd_undo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove one from a scorecard category."""
    if not is_authorized(update):
        return

    text = " ".join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text("Usage: `/undo gmb` or `/undo tiktok`", parse_mode=ParseMode.MARKDOWN)
        return

    category, _, _ = parse_done_input(text)
    if not category:
        await update.message.reply_text("Couldn't parse that. Try `/undo gmb`, `/undo tiktok`, etc.", parse_mode=ParseMode.MARKDOWN)
        return

    state = get_week_state()
    current = state["counts"].get(category, 0)
    if current > 0:
        state["counts"][category] = current - 1
        save_state(state)
        label = WEEKLY_TARGETS[category]["label"]
        await update.message.reply_text(f"Removed 1 from {label}. Now: {current - 1}/{WEEKLY_TARGETS[category]['target']}")
    else:
        await update.message.reply_text(f"{WEEKLY_TARGETS[category]['label']} is already at 0.")


async def cmd_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    topic = " ".join(context.args) if context.args else "choose the best topic for today based on pillar rotation"
    prompt = (
        f"Write a complete TikTok script for Taylor Dasch. Topic: {topic}\n\n"
        f"Include:\n"
        f"1. HOOK (first 3 seconds — text overlay + verbal)\n"
        f"2. BODY (beats with 7-second pattern interrupts noted)\n"
        f"3. CTA (DM keyword trigger)\n"
        f"4. CAPTION (punchy, 1-3 sentences)\n"
        f"5. HASHTAGS (5-10, three-tier system)\n"
        f"6. POSTING WINDOW (today's optimal time)\n"
        f"7. EDITING NOTES (what to do in CapCut)\n\n"
        f"Today is {datetime.now(TIMEZONE).strftime('%A')}."
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    prompt = (
        "Generate this week's full content calendar for Taylor Dasch.\n\n"
        "For each day Monday-Friday (+ optional Sat/Sun), include:\n"
        "- TikTok: pillar, hook, format, posting window, CTA keyword, hashtags\n"
        "- Instagram Reels: caption style note\n"
        "- YouTube Shorts: search-optimized title\n"
        "- GMB: theme for daily post\n"
        "- Any BP/Reddit targets\n"
        "- Tuesday: include Deal of the Week plan\n"
        "- Tuesday + Friday: filming day shot list\n\n"
        "Ensure pillar rotation (never 2 same pillars in a row).\n"
        f"This week starts {datetime.now(TIMEZONE).strftime('%A, %B %d, %Y')}."
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_gmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    day = datetime.now(TIMEZONE).strftime("%A")
    prompt = (
        f"Write today's Google My Business post for Taylor Dasch.\n"
        f"Today is {day}.\n\n"
        f"Format: Bible verse + Business Acumen Micro-Lesson (2-4 sentences connecting the verse to a real estate/business principle).\n"
        f"Include a soft CTA (newsletter, neighborhood guide, or Deal Analyzer).\n"
        f"Remind to upload a geotagged photo."
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_dotw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    details = " ".join(context.args) if context.args else None
    if not details:
        await update.message.reply_text(
            "Send me the deal details:\n"
            "`/dotw [address], [price], [bed/bath], [neighborhood], [any notes]`\n\n"
            "Example:\n"
            "`/dotw 1506 S 9th St, $140K, 3/2, South Temple, MTR/LTR play`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    prompt = (
        f"Create a Deal of the Week package for Taylor Dasch.\n"
        f"Deal details: {details}\n\n"
        f"Generate ALL of these:\n"
        f"1. YouTube video script outline (8-12 min) with entity declaration, numbers breakdown, verdict\n"
        f"2. Blog post outline (2,000+ words, H2s as questions, FAQ schema)\n"
        f"3. 60-second Short/Reel script\n"
        f"4. Social post caption (both relocator and investor frames)\n\n"
        f"Run the numbers with Bell County defaults (tax ~2.4-2.7%, insurance ~$1,200/yr, PM 10%, vacancy 8%, maintenance 5%).\n"
        f"Include honest verdict — would Taylor buy it? Scars and All."
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    topic = " ".join(context.args) if context.args else "choose the best topic for this week"
    prompt = (
        f"Write a complete YouTube description for Taylor Dasch.\n"
        f"Video topic: {topic}\n\n"
        f"Follow the 7-section template:\n"
        f"1. Direct answer (2-3 sentences, data-rich)\n"
        f"2. 'In this video' context paragraph\n"
        f"3. Key Points with timestamps (generate plausible timestamps)\n"
        f"4. Areas Discussed\n"
        f"5. Market Data Referenced\n"
        f"6. About Taylor Dasch section\n"
        f"7. Contact info + links\n\n"
        f"Also generate a pinned comment (newsletter/lead magnet plug).\n"
        f"Determine which channel this belongs on: Living in Temple or Investing in Temple."
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_newsletter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    topic = " ".join(context.args) if context.args else "choose the best topic based on current market conditions"
    prompt = (
        f"Draft this week's newsletter for Taylor Dasch.\n"
        f"Topic direction: {topic}\n\n"
        f"Include all 3 sections:\n"
        f"1. THE DEEP DIVE (~400 words) — hyperlocal analysis, answer-first\n"
        f"2. THE DEAL AUTOPSY — one property with real numbers + Scars and All verdict\n"
        f"3. BELL COUNTY BULLETIN — 3-5 bullets, one sentence each with data\n\n"
        f"Also provide:\n"
        f"- 3 subject line options using different formulas\n"
        f"- Preview text (40 chars)\n"
        f"- Universal market header (150 words)"
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_hooks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    pillar = " ".join(context.args) if context.args else "all pillars"
    prompt = (
        f"Generate 5 new TikTok hooks for Taylor Dasch.\n"
        f"Pillar: {pillar}\n\n"
        f"Each hook should:\n"
        f"- Stop the scroll in 3 seconds\n"
        f"- Include a specific number, location, or surprising claim\n"
        f"- Be different from the existing hook bank\n"
        f"- Work as both verbal delivery AND text overlay\n\n"
        f"Format: Hook text + suggested format (talking head/tour/green screen) + DM keyword CTA"
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_reddit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    topic = " ".join(context.args) if context.args else "investing in Central Texas rental properties"
    prompt = (
        f"Draft a Reddit reply for Taylor Dasch.\n"
        f"Topic/question: {topic}\n\n"
        f"Follow the 3-part Reddit reply framework:\n"
        f"1. Validate the question (1-2 sentences)\n"
        f"2. The Meat (200-400 words) — hyperlocal data, specific streets, real numbers\n"
        f"3. Soft close\n\n"
        f"Reddit is currently in Month 1 ramp — NO links, NO newsletter mentions. Pure value only.\n"
        f"Tone: helpful community member who happens to be deeply knowledgeable, NOT self-promotional."
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_bp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    topic = " ".join(context.args) if context.args else "Temple TX investment opportunity analysis"
    prompt = (
        f"Draft a BiggerPockets forum reply for Taylor Dasch.\n"
        f"Topic/question: {topic}\n\n"
        f"Rules:\n"
        f"- Answer with specific data (cap rates, rents, prices)\n"
        f"- Reference actual investor experience ($27M+, 100+ transactions)\n"
        f"- Link to blog posts when relevant (NOT promotional)\n"
        f"- NO video links (BP doesn't allow)\n"
        f"- Data-heavy, numbers-first\n"
        f"- Position as fellow investor sharing real experience, not agent soliciting"
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


async def cmd_repurpose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    # Use last assistant message as source content
    history = chat_history.get(update.message.chat_id, [])
    last_content = None
    for msg in reversed(history):
        if msg["role"] == "assistant":
            last_content = msg["content"]
            break

    if not last_content:
        await update.message.reply_text("No recent content to repurpose. Send me something first, then /repurpose it.")
        return

    prompt = (
        f"Repurpose this content for ALL platforms. Original content:\n\n"
        f"{last_content[:3000]}\n\n"
        f"Generate:\n"
        f"1. Instagram Reels caption (longer story-style, IG-specific hashtags)\n"
        f"2. YouTube Shorts title + description (search-optimized, must include 'Temple TX')\n"
        f"3. BiggerPockets forum version (data-heavy, NO video links)\n"
        f"4. GMB post version (Bible verse tie-in + micro-lesson)\n"
        f"5. Newsletter snippet version\n\n"
        f"Apply Framing Effect where possible:\n"
        f"- Relocator frame: community vitality, family impact\n"
        f"- Investor frame: macro-economics, rental demand, appreciation"
    )
    response = await ask_claude(update.message.chat_id, prompt)
    await send_response(update, response)


# ---------------------------------------------------------------------------
# Scheduled autopilot jobs
# ---------------------------------------------------------------------------
async def scheduled_gmb(context: ContextTypes.DEFAULT_TYPE):
    """Daily 6 AM CT — send GMB post draft."""
    chat_id = context.job.data
    day = datetime.now(TIMEZONE).strftime("%A")
    prompt = (
        f"Write today's Google My Business post for Taylor Dasch. Today is {day}.\n"
        f"Format: Bible verse + Business Acumen Micro-Lesson.\n"
        f"Include soft CTA and geotagged photo reminder."
    )
    response = await ask_claude(chat_id, prompt)
    for chunk in split_message(f"*Good morning! Here's today's GMB post:*\n\n{response}"):
        try:
            await context.bot.send_message(chat_id, chunk, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await context.bot.send_message(chat_id, chunk)


async def scheduled_calendar(context: ContextTypes.DEFAULT_TYPE):
    """Monday 6 AM CT — send weekly content calendar."""
    chat_id = context.job.data
    prompt = (
        "Generate this week's full content calendar for Taylor Dasch.\n"
        "Include TikTok (pillar, hook, format, time, hashtags), IG Reels, YT Shorts, GMB themes, "
        "BP/Reddit targets, filming day plans for Tuesday and Friday.\n"
        "Ensure pillar rotation.\n"
        f"Week of {datetime.now(TIMEZONE).strftime('%B %d, %Y')}."
    )
    response = await ask_claude(chat_id, prompt)
    for chunk in split_message(f"*Monday Content Calendar:*\n\n{response}"):
        try:
            await context.bot.send_message(chat_id, chunk, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await context.bot.send_message(chat_id, chunk)


async def scheduled_filming(context: ContextTypes.DEFAULT_TYPE):
    """Tuesday 6 AM CT — send filming day scripts."""
    chat_id = context.job.data
    prompt = (
        "Today is FILMING DAY for Taylor Dasch.\n\n"
        "Generate:\n"
        "1. Shot list for 3 TikToks (different pillars, outfit change reminders)\n"
        "2. Hook + script for each TikTok\n"
        "3. B-roll shot list (neighborhoods, streets, restaurants)\n"
        "4. Deal of the Week video outline (if applicable)\n"
        "5. Equipment checklist reminder (4K, vertical crop, gimbal for tours)"
    )
    response = await ask_claude(chat_id, prompt)
    for chunk in split_message(f"*Filming Day! Here's your shot list:*\n\n{response}"):
        try:
            await context.bot.send_message(chat_id, chunk, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await context.bot.send_message(chat_id, chunk)


async def scheduled_scorecard(context: ContextTypes.DEFAULT_TYPE):
    """Friday 5 PM CT — send automated weekly scorecard."""
    chat_id = context.job.data

    # Generate the scorecard with YouTube scan
    scorecard = format_scorecard(include_yt_scan=True)

    for chunk in split_message(scorecard):
        try:
            await context.bot.send_message(chat_id, chunk, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await context.bot.send_message(chat_id, chunk)

    # Follow up with AI analysis of the week
    state = get_week_state()
    counts = state.get("counts", {})
    items = state.get("items", [])

    prompt = (
        f"Analyze Taylor's content production this week and give brief, actionable feedback.\n\n"
        f"Production counts: {json.dumps(counts)}\n"
        f"Items completed: {json.dumps(items[-15:])}\n"
        f"Targets: {json.dumps({k: v['target'] for k, v in WEEKLY_TARGETS.items()})}\n\n"
        f"In 3-5 bullet points:\n"
        f"1. What went well (be specific)\n"
        f"2. Biggest gap and how to close it next week\n"
        f"3. One specific content idea for next week based on what performed well\n"
        f"Keep it punchy — this is a Friday evening quick-read."
    )
    response = await ask_claude(chat_id, prompt)
    for chunk in split_message(f"\n*Analysis:*\n\n{response}"):
        try:
            await context.bot.send_message(chat_id, chunk, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await context.bot.send_message(chat_id, chunk)


async def setup_autopilot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register scheduled jobs for this chat after /start."""
    chat_id = update.message.chat_id
    job_queue = context.application.job_queue

    # Remove existing jobs for this chat
    for job in job_queue.jobs():
        if job.data == chat_id:
            job.schedule_removal()

    # Daily GMB at 6:00 AM CT
    job_queue.run_daily(
        scheduled_gmb,
        time=time(hour=6, minute=0, tzinfo=TIMEZONE),
        data=chat_id,
        name=f"gmb_{chat_id}",
    )

    # Monday calendar at 6:00 AM CT
    job_queue.run_daily(
        scheduled_calendar,
        time=time(hour=6, minute=0, tzinfo=TIMEZONE),
        days=(0,),  # Monday
        data=chat_id,
        name=f"calendar_{chat_id}",
    )

    # Tuesday filming scripts at 6:00 AM CT
    job_queue.run_daily(
        scheduled_filming,
        time=time(hour=6, minute=0, tzinfo=TIMEZONE),
        days=(1,),  # Tuesday
        data=chat_id,
        name=f"filming_{chat_id}",
    )

    # Friday scorecard at 5:00 PM CT (replaces old blank review)
    job_queue.run_daily(
        scheduled_scorecard,
        time=time(hour=17, minute=0, tzinfo=TIMEZONE),
        days=(4,),  # Friday
        data=chat_id,
        name=f"scorecard_{chat_id}",
    )

    logger.info(f"Autopilot scheduled for chat {chat_id}")


# Wrap /start to also set up autopilot
async def cmd_start_with_autopilot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_start(update, context)
    if is_authorized(update):
        await setup_autopilot(update, context)


# ---------------------------------------------------------------------------
# Free-form message handler
# ---------------------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    response = await ask_claude(update.message.chat_id, update.message.text)
    await send_response(update, response)


# ---------------------------------------------------------------------------
# Error handler
# ---------------------------------------------------------------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception: {context.error}", exc_info=context.error)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    import asyncio
    # Python 3.14+ requires explicit event loop creation
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start_with_autopilot))
    app.add_handler(CommandHandler("scorecard", cmd_scorecard))
    app.add_handler(CommandHandler("done", cmd_done))
    app.add_handler(CommandHandler("undo", cmd_undo))
    app.add_handler(CommandHandler("tiktok", cmd_tiktok))
    app.add_handler(CommandHandler("calendar", cmd_calendar))
    app.add_handler(CommandHandler("gmb", cmd_gmb))
    app.add_handler(CommandHandler("dotw", cmd_dotw))
    app.add_handler(CommandHandler("youtube", cmd_youtube))
    app.add_handler(CommandHandler("newsletter", cmd_newsletter))
    app.add_handler(CommandHandler("hooks", cmd_hooks))
    app.add_handler(CommandHandler("reddit", cmd_reddit))
    app.add_handler(CommandHandler("bp", cmd_bp))
    app.add_handler(CommandHandler("repurpose", cmd_repurpose))

    # Free-form messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error_handler)

    # Register bot commands for Telegram's menu
    async def post_init(application):
        await application.bot.set_my_commands([
            BotCommand("start", "Start + activate autopilot"),
            BotCommand("scorecard", "Weekly production scorecard"),
            BotCommand("done", "Mark content as done"),
            BotCommand("undo", "Remove one from category"),
            BotCommand("tiktok", "TikTok script [topic]"),
            BotCommand("calendar", "Weekly content calendar"),
            BotCommand("gmb", "Today's GMB post"),
            BotCommand("dotw", "Deal of the Week [details]"),
            BotCommand("youtube", "YouTube description [topic]"),
            BotCommand("newsletter", "Newsletter draft [topic]"),
            BotCommand("hooks", "Generate hooks [pillar]"),
            BotCommand("reddit", "Reddit reply [topic]"),
            BotCommand("bp", "BiggerPockets reply [topic]"),
            BotCommand("repurpose", "Repurpose last content"),
        ])

    app.post_init = post_init

    logger.info("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
