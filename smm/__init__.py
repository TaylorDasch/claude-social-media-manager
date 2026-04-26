"""Social Media Manager operational layer for Taylor Dasch / EG Realty.

Thin CLI + SQLite-backed drafts/approval queue that wraps the existing
Content OS (skills, governance, content-registry.csv). Generators live
in `skills/` (invoked via Claude Code); this package is the plumbing
that turns skill output into approved, exportable content.
"""

__version__ = "0.1.0"

AUDIENCES = (
    "investor",
    "bsw_relocation",
    "fort_hood",
    "local_buyer",
    "seller",
    "homeowner",
    "agent_referral",
    "general_local",
)

FUNNEL_STAGES = (
    "awareness",
    "education",
    "trust",
    "conversion",
    "retargeting",
    "nurture",
)

PLATFORMS = (
    "facebook_personal",
    "facebook_business",
    "instagram_caption",
    "instagram_reel",
    "linkedin",
    "youtube_long",
    "youtube_short",
    "youtube_community",
    "gmb",
    "biggerpockets",
    "reddit",
    "email",
    "sms",
    "x_twitter",
    "tiktok",
    "blog",
    "newsletter_temple_insider",
    "newsletter_investor_brief",
)

DRAFT_STATUSES = (
    "draft",
    "needs_review",
    "approved",
    "scheduled",
    "posted",
    "rejected",
)
