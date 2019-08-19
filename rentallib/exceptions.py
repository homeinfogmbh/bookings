"""Common Exceptions."""


__all__ = [
    'RentingError',
    'EndBeforeStart',
    'DurationTooLong',
    'DurationTooShort',
    'AlreadyRented'
]


class RentingError(Exception):
    """Common error during renting."""


class EndBeforeStart(RentingError):
    """Indicates that the start datetime of the renting
    is greater than the end datetime of the reting.
    """


class DurationTooLong(RentingError):
    """Indicates that the rental duration is too long."""

    def __init__(self, max_duration):
        """Sets the maximum duration in minutes."""
        super().__init__()
        self.max_duration = max_duration


class DurationTooShort(RentingError):
    """Indicates that the rental duration is too short."""

    def __init__(self, min_duration):
        """Sets the minimum duration in minutes."""
        super().__init__()
        self.min_duration = min_duration


class AlreadyRented(RentingError):
    """Indicates that the rentable is already rented at this time."""

    def __init__(self, reservation):
        """Sets the conflicting reservation."""
        super().__init__()
        self.reservation = reservation
