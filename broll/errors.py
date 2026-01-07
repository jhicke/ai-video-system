# services/broll/errors.py


class BrollError(Exception):
    """Base class for all B-roll service errors."""


class BrollGenerationError(BrollError):
    """Raised when clip generation fails."""


class BrollCacheError(BrollError):
    """Raised when cache read/write fails."""


class BrollConfigError(BrollError):
    """Raised when configuration is invalid."""
