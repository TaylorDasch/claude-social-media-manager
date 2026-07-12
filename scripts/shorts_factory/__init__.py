"""Local, approval-gated long-form to shorts analysis engine.

Analysis stops at review manifests. A separate checksum-locked module can create
Postiz drafts only after Taylor approves an exact render; it never schedules or
publishes content.
"""

from .state import ALL_STATES

__all__ = ["ALL_STATES"]
__version__ = "1.0.0"
