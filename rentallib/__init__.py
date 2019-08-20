"""Library for renting stuff via digital signage systems."""

from rentallib.exceptions import RentingError
from rentallib.exceptions import EndBeforeStart
from rentallib.exceptions import DurationTooLong
from rentallib.exceptions import DurationTooShort
from rentallib.exceptions import AlreadyRented
from rentallib.orm import Rentable
from rentallib.orm import Renting


__all__ = [
    'RentingError',
    'EndBeforeStart',
    'DurationTooLong',
    'DurationTooShort',
    'AlreadyRented',
    'Rentable',
    'Renting'
]