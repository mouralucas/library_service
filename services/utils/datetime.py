from datetime import UTC, date, datetime


def utc_timestamp() -> datetime:
    """
    Returns the current UTC timestamp.
    """
    return datetime.now(UTC)


def current_date() -> date:
    """
    Returns the current date.
    Used for callable date fields.
    """
    return datetime.now().date()
