from datetime import datetime, date, UTC

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