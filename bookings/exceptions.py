"""Common Exceptions."""


__all__ = [
    'BookingError',
    'EndBeforeStart',
    'DurationTooLong',
    'DurationTooShort',
    'AlreadyBooked'
]


class BookingError(Exception):
    """Common error during booking."""


class EndBeforeStart(BookingError):
    """Indicates that the start datetime of the booking
    is greater than the end datetime of the booking.
    """


class DurationTooLong(BookingError):
    """Indicates that the booking duration is too long."""

    def __init__(self, max_duration):
        """Sets the maximum duration in minutes."""
        super().__init__()
        self.max_duration = max_duration


class DurationTooShort(BookingError):
    """Indicates that the booking duration is too short."""

    def __init__(self, min_duration):
        """Sets the minimum duration in minutes."""
        super().__init__()
        self.min_duration = min_duration


class AlreadyBooked(BookingError):
    """Indicates that a bookable is already booked at this time."""

    def __init__(self, booking):
        """Sets the conflicting booking."""
        super().__init__()
        self.booking = booking
