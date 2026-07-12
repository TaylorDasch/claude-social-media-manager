"""Shorts factory domain errors."""


class ShortsFactoryError(RuntimeError):
    """Base error for an actionable pipeline failure."""


class CommandError(ShortsFactoryError):
    """An external command failed or is unavailable."""


class ModelOutputError(ShortsFactoryError):
    """A model response failed strict JSON/schema validation."""


class ManifestError(ShortsFactoryError):
    """A manifest is missing, corrupt, or incompatible."""


class RevisionConflict(ManifestError):
    """The caller attempted to update a stale manifest revision."""


class InvalidTransition(ManifestError):
    """A requested workflow state transition is not allowed."""
