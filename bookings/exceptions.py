"""Common Exceptions."""


__all__ = [
    'AlreadyBooked',
    'DurationTooLong',
    'DurationTooShort',
    'EndBeforeStart'
]


class AlreadyBooked(Exception):
    """Indicates that a bookable is already booked at this time."""

    def __init__(self, conflicts: list):
        """Sets the conflicting bookings."""
        super().__init__()
        self.conflicts = conflicts


class DurationTooLong(Exception):
    """Indicates that the booking duration is too long."""

    def __init__(self, max_duration: int):
        """Sets the maximum duration in minutes."""
        super().__init__()
        self.max_duration = max_duration


class DurationTooShort(Exception):
    """Indicates that the booking duration is too short."""

    def __init__(self, min_duration: int):
        """Sets the minimum duration in minutes."""
        super().__init__()
        self.min_duration = min_duration


class EndBeforeStart(Exception):
    """Indicates that the start datetime of the booking
    is greater than the end datetime of the booking.
    """
